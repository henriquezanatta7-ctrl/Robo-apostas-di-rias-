import os
import json
import google.generativeai as genai

GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_KEY:
    raise ValueError("Chave GEMINI_API_KEY nao encontrada!")

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def gerar_analise(jogo, liga, horario, odds):
    prompt = f"""
    Analise o jogo {jogo} ({liga}, {horario}) com odds {odds}.
    Retorne EXCLUSIVAMENTE um JSON valido com as chaves:
    "jogo", "liga", "clima_e_gramado", "desfalques_e_escalacao", 
    "historico_e_momento", "palpite_recomendado", "odd_estimada", 
    "nivel_confianca", "stake_sugerida_reais", "resumo_analise".
    """
    try:
        res = model.generate_content(prompt)
        txt = res.text.replace("```json", "").replace("```", "").strip()
        return json.loads(txt)
    except Exception as e:
        print(f"Erro em {jogo}: {e}")
        return None

def main():
    jogos = [
        {"jogo": "Flamengo vs Chapecoense", "liga": "Brasileirao", "horario": "21:30", "odds": "1.55 / 3.80 / 6.50"},
        {"jogo": "Coritiba vs Palmeiras", "liga": "Brasileirao", "horario": "19:30", "odds": "3.60 / 3.40 / 2.10"},
        {"jogo": "Ind. Medellin vs Vasco", "liga": "Sul-Americana", "horario": "19:00", "odds": "2.10 / 3.20 / 3.50"}
    ]
    relatorio = []
    for j in jogos:
        res = gerar_analise(j["jogo"], j["liga"], j["horario"], j["odds"])
        if res:
            relatorio.append(res)
    
    with open("dados_jogos_hoje.json", "w", encoding="utf-8") as f:
        json.dump(relatorio, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
