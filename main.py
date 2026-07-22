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
    Você é um analista esportivo chefe. Analise a partida:
    Jogo: {jogo}
    Liga: {liga}
    Horário: {horario}
    Odds: {odds}

    Retorne EXCLUSIVAMENTE um JSON válido com exatamente estas chaves:
    {{
      "jogo": "{jogo}",
      "liga": "{liga}",
      "clima_e_gramado": "Análise sobre o clima da cidade hoje (ex: chuva forte, vento) e o impacto direto no gramado/gols",
      "desfalques_e_escalacao": "Principais desfalques, retornos e ajuste tático dos técnicos",
      "historico_e_momento": "Momento recente dos dois times",
      "palpite_recomendado": "O mercado com melhor valor para apostar",
      "odd_estimada": "Odd aproximada",
      "nivel_confianca": "Alta, Média ou Muito Alto",
      "resumo_analise": "Justificativa tática aprofundada unindo clima, momento e estatística"
    }}
    """
    try:
        res = model.generate_content(prompt)
        txt = res.text.replace("```json", "").replace("```", "").strip()
        return json.loads(txt)
    except Exception as e:
        print(f"Erro em {jogo}: {e}")
        return None

def main():
    # Grade completa com os principais jogos da rodada
    jogos = [
        {"jogo": "Chapecoense vs Flamengo", "liga": "Brasileirão Série A", "horario": "21:30", "odds": "Fla 1.55 / Empate 3.80"},
        {"jogo": "Coritiba vs Palmeiras", "liga": "Brasileirão Série A", "horario": "19:30", "odds": "Palmeiras 2.10 / Empate 3.40"},
        {"jogo": "São Paulo vs Athletico-PR", "liga": "Brasileirão Série A", "horario": "21:30", "odds": "São Paulo 1.85 / Empate 3.30"},
        {"jogo": "Ind. Medellín vs Vasco", "liga": "Copa Sul-Americana", "horario": "19:00", "odds": "DIM 2.10 / Vasco 3.50"},
        {"jogo": "Lanús vs Cienciano", "liga": "Copa Sul-Americana", "horario": "21:30", "odds": "Lanús 1.40 / Empate 4.20"},
        {"jogo": "Inter Miami vs Chicago Fire", "liga": "MLS (EUA)", "horario": "20:30", "odds": "Inter Miami 1.45"},
        {"jogo": "NY Liberty vs Chicago Sky", "liga": "WNBA (Basquete)", "horario": "20:00", "odds": "NY Liberty 1.20"},
        {"jogo": "Rangers vs White Sox", "liga": "MLB (Beisebol)", "horario": "21:05", "odds": "Rangers 1.55"}
    ]
    
    relatorio = []
    for j in jogos:
        print(f"Gerando análise para {j['jogo']}...")
        res = gerar_analise(j["jogo"], j["liga"], j["horario"], j["odds"])
        if res:
            relatorio.append(res)
    
    with open("dados_jogos_hoje.json", "w", encoding="utf-8") as f:
        json.dump(relatorio, f, ensure_ascii=False, indent=2)
    print("Sucesso! JSON atualizado.")

if __name__ == "__main__":
    main()
