class SequenceParser:
    def __init__(self, filepath):
        self.filepath = filepath

    def parse_genbank_auto(self):
        """
        Membaca 1 file GenBank gelondongan, lalu otomatis memotong 
        menjadi list ekson dan intron berdasarkan koordinat fitur.
        """
        full_sequence = ""
        features = []
        origin_zone = False

        with open(self.filepath, 'r') as file:
            for line in file:
                # 1. Ambil baris koordinat fitur (FEATURES)
                if line.startswith("     exon ") or line.startswith("     intron "):
                    parts = line.strip().split()
                    tipe_fitur = parts[0] # 'exon' atau 'intron'
                    koordinat_raw = parts[1] # contoh: '1..142' atau 'join(1..10,20..30)'
                    
                    # Bersihkan koordinat jika ada karakter join atau complement
                    koordinat_clean = koordinat_raw.replace("join(", "").replace(")", "").replace("complement(", "")
                    
                    # Ambil angka awal dan akhir lokasi pemotongan
                    try:
                        if ".." in koordinat_clean:
                            # Jika ada beberapa potongan (join), ambil yang pertama untuk simplifikasi tugas
                            if "," in koordinat_clean:
                                koordinat_clean = koordinat_clean.split(",")[0]
                            start_pos, end_pos = koordinat_clean.split("..")
                            
                            # Bersihkan karakter non-angka seperti < atau >
                            start_int = int(''.join(filter(str.isdigit, start_pos)))
                            end_int = int(''.join(filter(str.isdigit, end_pos)))
                            
                            features.append({
                                "type": tipe_fitur,
                                "start": start_int,
                                "end": end_int
                            })
                    except Exception:
                        continue
                
                # 2. Ambil untai sekuens DNA utuh di bagian bawah (ORIGIN)
                if line.startswith("ORIGIN"):
                    origin_zone = True
                    continue
                if line.startswith("//"):
                    origin_zone = False
                
                if origin_zone:
                    # Buang nomor baris dan spasi dari zona ORIGIN
                    clean_line = ''.join([char for char in line if char.isalpha()]).upper()
                    full_sequence = full_sequence + clean_line

        # 3. Proses Pemotongan Otomatis Untai DNA Berdasarkan Peta Fitur
        cut_sequences = []
        counter_exon = 1
        counter_intron = 1

        for feat in features:
            # Indeks Python dimulai dari 0, sedangkan koordinat NCBI dimulai dari 1
            start_idx = feat["start"] - 1
            end_idx = feat["end"]
            
            # Ekstraksi/potong string sekuens secara langsung!
            sliced_seq = full_sequence[start_idx:end_idx]
            
            if sliced_seq:
                if feat["type"] == "exon":
                    header_name = f"HBB_exon_{counter_exon}_(Auto_Cut)"
                    counter_exon += 1
                else:
                    header_name = f"HBB_intron_{counter_intron}_(Auto_Cut)"
                    counter_intron += 1
                    
                cut_sequences.append({
                    "header": header_name,
                    "sequence": sliced_seq
                })
                
        return cut_sequences


class SequenceAnalyzer:
    def count_nucleotides(self, sequence):
        counts = {"A": 0, "T": 0, "G": 0, "C": 0}
        for base in sequence:
            if base in counts:
                counts[base] = counts[base] + 1
        return counts

    def calculate_gc_content(self, sequence):
        if len(sequence) == 0:
            return 0.0
        counts = self.count_nucleotides(sequence)
        gc_count = counts["G"] + counts["C"]
        return (gc_count / len(sequence)) * 100