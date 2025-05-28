import pandas as pd
import streamlit as st

def carregar_dados():
    try:
        df = pd.read_csv('dogs.csv', encoding='utf-8')
    except Exception as e:
        st.error(f"Erro ao carregar arquivo: {e}")
        st.stop()

    if 'Nome' not in df.columns:
        st.error("Erro: coluna 'Nome' não encontrada no CSV.")
        st.stop()

    df.set_index('Nome', inplace=True)
    return df.to_dict(orient='index')

def quiz():
    st.title("🐶 Quiz: Qual é a raça de cachorro ideal para você?")
    st.write("Responda às perguntas abaixo e descubra a raça de cachorro que mais combina com você!")

    respostas = {
        'porte': st.selectbox("Porte do cachorro:", ["Pequeno", "Pequeno-Médio", "Médio", "Grande"]),
        'tipo': st.selectbox("Tipo de cachorro:", ["Caça", "Trabalhador", "Terrier", "Pastor", "Esportista", "Não esportista", "Standart", "Toy"]),
        'amigavel': st.slider("Nível de amigabilidade:", 1, 5, 3),
        'treinamento': st.slider("Importância do treinamento:", 1, 5, 3),
        'tosa': st.selectbox("Necessidade de tosa:", ["Pequena", "Média", "Grande", "Muito grande"]),
        'criancas': st.radio("Bom com crianças:", ["Sim", "Não", "Sim, mesmo que precise treinar"]),
        'inteligencia': st.slider("Nível de inteligência:", 1, 5, 3),
        'pelo': st.selectbox("Processo de troca de pelo:", ["Pequeno", "Médio", "Grande", "Muito grande"])
    }

    if st.button("🔍 Descobrir minha raça ideal"):
        racas = carregar_dados()
        melhor_raca = None
        melhor_pontos = -1

        for nome_raca, dados in racas.items():
            pontos = 0

            if 'Porte' in dados and dados['Porte'].strip().lower() == respostas['porte'].strip().lower():
                pontos += 2
            if 'Tipo' in dados and dados['Tipo'].strip().lower() == respostas['tipo'].strip().lower():
                pontos += 1
            if 'Amigavel (1-10)' in dados and abs(dados['Amigavel (1-10)'] - respostas['amigavel']) <= 1:
                pontos += 1
            if 'Dificuldade de Treino (1-10)' in dados and dados['Dificuldade de Treino (1-10)'] >= respostas['treinamento']:
                pontos += 1
            if 'Necessidade de Tosa' in dados and dados['Necessidade de Tosa'].strip().lower() == respostas['tosa'].strip().lower():
                pontos += 2
            if 'Bom com Crianças' in dados:
                crianca_ok = (
                    (respostas['criancas'] == 'Sim' and dados['Bom com Crianças'] == 'Sim') or
                    (respostas['criancas'] == 'Sim, mesmo que precise treinar' and dados['Bom com Crianças'] in ['Sim', 'Caso treinado'])
                )
                if crianca_ok:
                    pontos += 2
            if 'Inteligência (1-10)' in dados and dados['Inteligência (1-10)'] >= respostas['inteligencia']:
                pontos += 1
            if 'Nível de Queda de Pelo' in dados and dados['Nível de Queda de Pelo'].strip().lower() == respostas['pelo'].strip().lower():
                pontos += 1

            if pontos > melhor_pontos:
                melhor_pontos = pontos
                melhor_raca = nome_raca

        if melhor_raca:
            st.success(f"✨ A raça que mais combina com você é: **{melhor_raca.upper()}** ({melhor_pontos}/10 pontos)")
            st.subheader("🐾 Características da raça:")
            for chave, valor in racas[melhor_raca].items():
                st.write(f"- **{chave}**: {valor}")
            link = f"https://pt.wikipedia.org/wiki/{melhor_raca.replace(' ', '_')}"
            st.markdown(f"[Saiba mais sobre {melhor_raca}]({link})")
        else:
            st.warning("Não conseguimos identificar uma raça ideal com base nas suas respostas. Tente novamente.")

# Executar o quiz
quiz()
