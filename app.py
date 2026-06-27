from flask import Flask, render_template, request, send_file
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from bioinformatics import SequenceParser, SequenceAnalyzer

app = Flask(__name__)

def ambil_nilai_gc(item):
    return item["gc_content"]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file_input = request.files['file_kamu']
        
        if file_input.filename != '':
            if not os.path.exists("static"):
                os.makedirs("static")
                
            filepath = os.path.join("static", file_input.filename)
            file_input.save(filepath)
            
            # Panggil fungsi parser otomatis GenBank terbaru kita
            parser_obj = SequenceParser(filepath)
            raw_data = parser_obj.parse_genbank_auto()
                
            analyzer_obj = SequenceAnalyzer()
            hasil_pipeline = []
            
            for item in raw_data:
                frekuensi_basa = analyzer_obj.count_nucleotides(item["sequence"])
                nilai_gc = analyzer_obj.calculate_gc_content(item["sequence"])
                
                hasil_data = {
                    "header": item["header"],
                    "sequence": item["sequence"],
                    "counts": frekuensi_basa,
                    "gc_content": nilai_gc
                }
                hasil_pipeline.append(hasil_data)
                
            # Urutkan berdasarkan GC content
            hasil_pipeline.sort(key=ambil_nilai_gc, reverse=True)
            
            # Pisahkan data untuk Top 3 Juara Komparasi Kontras
            list_ekson = [item for item in hasil_pipeline if "exon" in item["header"].lower()]
            list_intron = [item for item in hasil_pipeline if "intron" in item["header"].lower()]
            
            top_2_ekson = list_ekson[0:2] if len(list_ekson) >= 2 else list_ekson
            top_1_intron = list_intron[-1:] if len(list_intron) >= 1 else list_intron
            top_3 = top_2_ekson + top_1_intron
            
            # Pembuatan Grafik Batang Matplotlib
            list_header = [item["header"] for item in hasil_pipeline]
            list_gc = [item["gc_content"] for item in hasil_pipeline]
            
            list_warna = []
            for item in hasil_pipeline:
                if "exon" in item["header"].lower():
                    list_warna.append('#b3cde3') # Biru untuk Ekson
                else:
                    list_warna.append('#fbb4ae') # Pink untuk Intron
            
            plt.figure(figsize=(9, 4.5))
            plt.bar(list_header, list_gc, color=list_warna, edgecolor='#4a4a4a', linewidth=1)
            plt.title('Perbandingan GC-Content: Hasil Pemotongan Otomatis GenBank', fontsize=12, fontweight='bold', color='#4b0082')
            plt.xlabel('Fragmen Hasil Potongan Sistem', fontsize=10, fontweight='bold')
            plt.ylabel('GC-Content (%)', fontsize=10, fontweight='bold')
            plt.xticks(rotation=15, ha='right', fontsize=9)
            plt.ylim(0, 100)
            plt.grid(axis='y', linestyle='--', alpha=0.5)
            plt.tight_layout()
            
            chart_path = os.path.join("static", "gc_chart.png")
            plt.savefig(chart_path)
            plt.close()
            
            # Tulis File CSV laporan keluar
            csv_path = os.path.join("static", "hasil_analisis.csv")
            with open(csv_path, "w") as f_csv:
                f_csv.write("Header,Panjang_Basa,GC_Content_Persen,A,T,G,C\n")
                for res in hasil_pipeline:
                    baris_teks = f"{res['header']},{len(res['sequence'])},{res['gc_content']:.2f},{res['counts']['A']},{res['counts']['T']},{res['counts']['G']},{res['counts']['C']}\n"
                    f_csv.write(baris_teks)
            
            if os.path.exists(filepath):
                os.remove(filepath)
                
            return render_template('index.html', hasil=hasil_pipeline, top_3_juara=top_3, ada_data=True)
            
    return render_template('index.html', hasil=None, top_3_juara=None, ada_data=False)

@app.route('/unduh-csv')
def unduh_csv():
    csv_path = os.path.join("static", "hasil_analisis.csv")
    if os.path.exists(csv_path):
        return send_file(csv_path, as_attachment=True)
    return "File tidak ditemukan.", 404

if __name__ == '__main__':
    app.run(debug=True)