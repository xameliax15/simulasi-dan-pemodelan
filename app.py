from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import io
import base64
from math import comb, pow

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    explanation = None
    image = None
    if request.method == "POST":
        try:
            n = int(request.form["n"])
            p = float(request.form["p"].replace(",", "."))
            k = int(request.form["k"])

            # Hitung probabilitas
            probability = comb(n, k) * pow(p, k) * pow(1 - p, n - k)

            # Langkah-langkah penjelasan
            explanation = (
                f"Langkah 1: Hitung Koefisien Binomial<br>"
                f"\\( C(n, k) = \\binom{{{n}}}{{{k}}} = {comb(n, k)} \\)<br><br>"
                f"Langkah 2: Substitusikan ke dalam Rumus<br>"
                f"\\( P(X = {k}) = \\binom{{{n}}}{{{k}}} \\cdot {p}^{{{k}}} \\cdot (1-{p})^{{{n-k}}} \\)<br><br>"
                f"Langkah 3: Hitung Probabilitas<br>"
                f"\\( P(X = {k}) = {probability:.4f} \\)<br>"
            )

            # Buat grafik
            x = list(range(n + 1))
            y = [comb(n, i) * pow(p, i) * pow(1 - p, n - i) for i in x]
            
            plt.bar(x, y, color="skyblue")
            plt.title("Distribusi Probabilitas Binomial")
            plt.xlabel("Jumlah Keberhasilan (k)")
            plt.ylabel("Probabilitas")
            plt.grid(axis="y", linestyle="--", alpha=0.7)

            # Simpan grafik sebagai string base64
            img = io.BytesIO()
            plt.savefig(img, format="png", bbox_inches="tight")
            img.seek(0)
            image = base64.b64encode(img.getvalue()).decode()
            img.close()
            plt.close()
        except ValueError:
            result = "Masukkan data yang valid!"

        result = f"Probabilitas untuk k = {k} adalah {probability:.4f}"

    return render_template("index.html", result=result, explanation=explanation, image=image)


if __name__ == '__main__':
    print("memulai aplikasi flask...")
    app.run(host='0.0.0.0', port=5000, debug=True)
    print("aplikasi flask berhenti")