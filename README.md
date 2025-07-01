# 📈 Sistema de Análise de Investimentos Brasil
Um sistema completo e profissional para análise de investimentos no mercado brasileiro, incluindo ações do Ibovespa, Fundos Imobiliários (FIIs) e Fundos de Investimento em Cadeias Produtivas Agroindustriais.
🚀 Características Principais
•	Análise Automatizada: Coleta dados em tempo real do Yahoo Finance
•	Score Inteligente: Sistema próprio de pontuação baseado em múltiplos indicadores
•	Interface Profissional: Design moderno e responsivo com Streamlit
•	Gráficos Interativos: Visualizações avançadas com Plotly
•	Recomendações IA: Sistema de recomendações baseado em análise técnica e fundamentalista
📊 O que o Sistema Analisa
Ações do Ibovespa (20 principais)
•	PETR4, VALE3, ITUB4, BBDC4, ABEV3, WEGE3, RENT3, LREN3, MGLU3, B3SA3
•	JBSS3, SUZB3, RAIL3, GGBR4, BBAS3, ELET3, SANB11, CSNA3, USIM5, CIEL3
Fundos Imobiliários (20 selecionados)
•	KNRI11, HGLG11, XPLG11, BCFF11, MXRF11, BTLG11, KNCR11, GGRC11, HGRU11, VILG11
•	XPML11, VISC11, HGRE11, RBRF11, PVBI11, RZTR11, RBRR11, JSRE11, RBRY11, TRXF11
Fundos Agroindustriais (20 selecionados)
•	FIAG11, AGRO11, RBBV11, SOJA11, BEEF11, CORN11, FAIR11, SCPF11, FOFT11, LFTT11
•	PATC11, GTWR11, TEPP11, SADI11, VRTA11, RFOF11, FCFL11, RBFF11, KDIF11, RBRD11
🔧 Instalação e Configuração
Pré-requisitos
•	Python 3.8 ou superior
•	pip (gerenciador de pacotes Python)
Passo 1: Clone ou baixe os arquivos
Salve os arquivos investment_analyzer.py e requirements.txt na mesma pasta.
Passo 2: Instale as dependências
pip install -r requirements.txt
Passo 3: Execute o sistema
streamlit run investment_analyzer.py

📋 Como Usar
1. Selecione o Tipo de Análise
•	Ações do Ibovespa: Análise focada nas principais ações da bolsa
•	Fundos Imobiliários: Análise dos melhores FIIs
•	Fundos Agroindustriais: Análise dos fundos do agronegócio
•	Análise Completa: Visão geral de todos os tipos de investimento
2. Configure o Período
•	6 meses, 1 ano, 2 anos ou 5 anos
•	Recomenda-se 1 ano para análise equilibrada
3. Clique em "Iniciar Análise"
O sistema coletará dados e apresentará:
•	Score de recomendação (0-100)
•	Gráficos de performance
•	Tabela detalhada com métricas
•	Recomendações específicas
📊 Metodologia do Score
Componentes do Score (0-100 pontos):
•	Tendência de Preço (30%): Performance no período analisado
•	Análise Técnica (25%): Posição relativa às médias móveis (20 e 50 períodos)
•	Volatilidade (20%): Menor volatilidade indica maior estabilidade
•	Liquidez (15%): Volume médio de negociação
•	Múltiplos (10%): P/L e outros indicadores fundamentalistas
Interpretação dos Resultados:
•	🟢 70-100 pontos: Compra Forte
•	🟡 50-69 pontos: Compra Moderada
•	🔴 0-49 pontos: Aguardar melhores condições
🎯 Funcionalidades Avançadas
Gráficos Interativos
•	Ranking por Score: Visualiza os melhores ativos
•	Performance Comparativa: Acompanha a evolução temporal
•	Análise de Tendências: Identifica padrões de mercado
Recomendações Inteligentes
•	Análise automática dos top 3 ativos
•	Justificativa baseada em dados
•	Estratégias de entrada sugeridas
Interface Responsiva
•	Design profissional com gradientes
•	Cards informativos coloridos
•	Métricas destacadas
⚠️ Avisos Importantes
1.	Não é Consultoria: Este sistema é para fins educacionais e informativos
2.	Risco de Investimento: Todo investimento envolve riscos
3.	Dados em Tempo Real: Os dados podem ter pequeno delay
4.	Consulte Profissionais: Sempre consulte um assessor de investimentos
🔧 Solução de Problemas
Erro de Conexão
•	Verifique sua conexão com a internet
•	Alguns provedores podem bloquear APIs financeiras
Dados Não Carregam
•	Tente novamente após alguns minutos
•	Alguns ativos podem estar temporariamente indisponíveis
Performance Lenta
•	Reduza o número de ativos analisados
•	Use períodos menores (6 meses)
🆙 Futuras Melhorias
•	[ ] Integração com mais fontes de dados
•	[ ] Análise de dividendos e proventos
•	[ ] Alertas automáticos
•	[ ] Exportação de relatórios PDF
•	[ ] Backtesting de estratégias
•	[ ] Análise setorial
📞 Suporte
Para dúvidas ou sugestões sobre o sistema, consulte a documentação das bibliotecas utilizadas:
•	Streamlit
•	YFinance
•	Plotly
________________________________________
💼 Desenvolvido para otimizar seus investimentos no mercado brasileiro 🇧🇷

