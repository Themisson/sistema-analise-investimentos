import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')
from datetime import datetime, timedelta
import time

# Configuração da página
st.set_page_config(
    page_title="📈 Análise de Investimentos Brasil",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para design profissional
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #1f4e79, #2e7d32);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem;
    }
    
    .recommendation-card {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        border-left: 5px solid #2e7d32;
    }
    
    .warning-card {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        padding: 1rem;
        border-radius: 10px;
        color: #333;
        margin: 1rem 0;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
</style>
""", unsafe_allow_html=True)

class InvestmentAnalyzer:
    def __init__(self):
        # Cache simples para evitar downloads repetidos
        if 'data_cache' not in st.session_state:
            st.session_state.data_cache = {}
        
        # Ações da B3 - Lista completa por segmentos (400+ ações)
        self.b3_stocks = [
            # Petróleo, Gás e Combustíveis
            'PETR3.SA', 'PETR4.SA', 'PRIO3.SA', 'RRRP3.SA', 'RECV3.SA', '3R11.SA',
            'UGPA3.SA', 'BRDT3.SA', 'VIBR3.SA', 'CSAN3.SA', 'DMVF3.SA',
            
            # Mineração e Siderurgia
            'VALE3.SA', 'CSNA3.SA', 'GGBR4.SA', 'USIM5.SA', 'GOAU4.SA', 'FESA4.SA',
            'JHSF3.SA', 'FHER3.SA', 'COCE5.SA', 'CGRA4.SA', 'BAUH4.SA',
            
            # Bancos
            'ITUB4.SA', 'BBDC4.SA', 'BBAS3.SA', 'SANB11.SA', 'BPAC11.SA', 'BRFS3.SA',
            'BMGB4.SA', 'BIDI11.SA', 'PINE4.SA', 'BPAN4.SA', 'BGIP4.SA', 'BRSR6.SA',
            
            # Seguros e Previdência
            'SULA11.SA', 'BBSE3.SA', 'PSSA3.SA', 'WIZS3.SA', 'IRFM3.SA',
            
            # Varejo e Comércio
            'MGLU3.SA', 'LREN3.SA', 'AMER3.SA', 'PCAR3.SA', 'VVAR3.SA', 'GUAR3.SA',
            'LJQQ3.SA', 'GRND3.SA', 'VIIA3.SA', 'AMAR3.SA', 'SOMA3.SA', 'TFCO4.SA',
            'NTCO3.SA', 'SMFT3.SA', 'CEAB3.SA', 'HBSA3.SA', 'MLAS3.SA',
            
            # Alimentação e Bebidas
            'ABEV3.SA', 'JBSS3.SA', 'BRFS3.SA', 'MRFG3.SA', 'SMLS3.SA', 'CAML3.SA',
            'BEEF3.SA', 'PNVL3.SA', 'MDIA3.SA', 'JALL3.SA', 'VULC3.SA', 'AMBP3.SA',
            
            # Tecnologia e Telecomunicações
            'VIVT3.SA', 'TIMS3.SA', 'DESK3.SA', 'TOTS3.SA', 'IFCM3.SA', 'LWSA3.SA',
            'MOVI3.SA', 'OIBR3.SA', 'OIBR4.SA', 'TELE3.SA', 'WSON33.SA',
            
            # Energia Elétrica
            'ELET3.SA', 'ELET6.SA', 'EQTL3.SA', 'CPFE3.SA', 'CMIG4.SA', 'CPLE6.SA',
            'TAEE11.SA', 'COCE5.SA', 'CEPE6.SA', 'CESP6.SA', 'CEGR3.SA', 'CLSC4.SA',
            'ENBR3.SA', 'ENGI11.SA', 'ENEV3.SA', 'NEOE3.SA', 'AURE3.SA',
            
            # Construção Civil e Materiais
            'MRVE3.SA', 'CYRE3.SA', 'EVEN3.SA', 'GFSA3.SA', 'JHSF3.SA', 'HBTS5.SA',
            'VIVR3.SA', 'PLPL3.SA', 'MOAR3.SA', 'TCSA3.SA', 'TRIS3.SA', 'RSID3.SA',
            'EZTC3.SA', 'DIRR3.SA', 'LAVV3.SA', 'MULT3.SA', 'BRAP4.SA', 'CRDE3.SA',
            'KLBN11.SA', 'SUZB3.SA', 'FIBR3.SA', 'DURA4.SA', 'TUPY3.SA',
            
            # Agronegócio
            'SLC3.SA', 'TERA3.SA', 'SOJA3.SA', 'LAND3.SA', 'RUMO3.SA', 'RAIZ4.SA',
            'FRAS3.SA', 'AGRO3.SA', 'MEAL3.SA', 'KEPL3.SA',
            
            # Transporte e Logística
            'RAIL3.SA', 'CCRO3.SA', 'LOGN3.SA', 'AZUL4.SA', 'GOLL4.SA', 'EMBR3.SA',
            'STBP3.SA', 'ECOR3.SA', 'ARML3.SA', 'JSLG3.SA', 'RLOG3.SA',
            
            # Papel e Celulose
            'KLBN11.SA', 'SUZB3.SA', 'FIBR3.SA', 'MELK3.SA', 'KROT3.SA',
            
            # Químicos e Petroquímicos
            'BRASKEM.SA', 'UNIP6.SA', 'UNIPAR.SA', 'OXTR3.SA', 'BRKM5.SA',
            
            # Saúde e Farmacêuticos
            'RAIA3.SA', 'PARD3.SA', 'DASA3.SA', 'FLRY3.SA', 'GNDI3.SA', 'AALR3.SA',
            'HAPV3.SA', 'QUAL3.SA', 'MATD3.SA', 'RDOR3.SA', 'ONCR3.SA', 'HYPE3.SA',
            'BLAU3.SA', 'ODPV3.SA', 'YDUQ3.SA',
            
            # Educação
            'COGN3.SA', 'YDUQ3.SA', 'SEER3.SA', 'ANIM3.SA', 'VIVA3.SA',
            
            # Têxtil e Vestuário
            'GUAR3.SA', 'FRAS3.SA', 'CAMB3.SA', 'COTEMINAS.SA', 'TECN3.SA',
            
            # Serviços Financeiros
            'B3SA3.SA', 'IRBR3.SA', 'CARD3.SA', 'RENT3.SA', 'LOCA3.SA',
            'MILS3.SA', 'CASH3.SA', 'ATOM3.SA', 'CTKA4.SA',
            
            # Utilities e Saneamento
            'SAPR11.SA', 'SBSP3.SA', 'CSMG3.SA', 'COPAS6.SA', 'SANE11.SA',
            
            # Metalurgia
            'GERDAU.SA', 'GGBR4.SA', 'CSNA3.SA', 'USIM5.SA', 'FESA4.SA', 'COCE5.SA',
            
            # Automobilístico
            'POMO4.SA', 'TUPY3.SA', 'LEVE3.SA', 'HBOR3.SA', 'RSID3.SA',
            
            # Madeira e Móveis
            'EUCL3.SA', 'EUCA4.SA',
            
            # Diversos
            'WEGE3.SA', 'RAPT4.SA', 'PSSA3.SA', 'TOTS3.SA', 'TPIS3.SA', 'SMTO3.SA',
            'CVCB3.SA', 'SHOW3.SA', 'BAHI3.SA', 'TEND3.SA', 'MTRE3.SA', 'ESPA3.SA',
            'JFEN3.SA', 'SOND6.SA', 'ITSA4.SA', 'BBDC3.SA', 'PETR3.SA', 'VALE5.SA',
            'CMIG3.SA', 'LIGHT.SA', 'GOAU3.SA', 'USIM3.SA', 'GGBR3.SA', 'CSNA3.SA',
            
            # Small Caps e outras
            'ABCB4.SA', 'ALPA4.SA', 'ALPK3.SA', 'ALUP11.SA', 'AMAR3.SA', 'AMBP3.SA',
            'ARZZ3.SA', 'ATOM3.SA', 'BBDC3.SA', 'BEEF3.SA', 'BEES3.SA', 'BEES4.SA',
            'BGIP3.SA', 'BMEB4.SA', 'BOBR4.SA', 'BRAP3.SA', 'BRDT3.SA', 'BRFS3.SA',
            'BRKM3.SA', 'BRSR3.SA', 'CAML3.SA', 'CBAV3.SA', 'CCPR3.SA', 'CEAB3.SA',
            'CGAS5.SA', 'CGRA3.SA', 'CHAP4.SA', 'CLSC3.SA', 'COCE3.SA', 'CORR4.SA',
            'CPLE3.SA', 'CSMG3.SA', 'CTKA3.SA', 'DEXP3.SA', 'DOHL4.SA', 'EALT4.SA',
            'EBTP4.SA', 'EEEL3.SA', 'ELET5.SA', 'ELPL4.SA', 'EMAE4.SA', 'ENMT4.SA',
            'EQMA3B.SA', 'ESTR4.SA', 'EUCA3.SA', 'FESA3.SA', 'FHER3.SA', 'FIQE3.SA',
            'FRTA3.SA', 'FVNA3.SA', 'GMAT3.SA', 'GOAU3.SA', 'GPAR3.SA', 'GRND3.SA',
            'GSHP3.SA', 'HAGA4.SA', 'HBRE3.SA', 'HETA4.SA', 'HGTX3.SA', 'IGBR3.SA',
            'IGTA3.SA', 'INEP4.SA', 'JOPA3.SA', 'KEPL3.SA', 'LEVE3.SA', 'LIGT3.SA',
            'LIPR3.SA', 'LOGN3.SA', 'LUPA3.SA', 'LUXM4.SA', 'MAGG3.SA', 'MBLY3.SA',
            'MEND6.SA', 'MMXM3.SA', 'MOAR3.SA', 'MYPK3.SA', 'NORD3.SA', 'OFSA3.SA',
            'OSXB3.SA', 'PATI4.SA', 'PDGR3.SA', 'PEAB4.SA', 'PINE4.SA', 'PMAM3.SA',
            'PNVL4.SA', 'POMO3.SA', 'PRBC4.SA', 'PSSA3.SA', 'RADL3.SA', 'RAPT3.SA',
            'RCSL4.SA', 'REDE4.SA', 'RIPI4.SA', 'SANB3.SA', 'SAPR4.SA', 'SAPR3.SA',
            'SBFG3.SA', 'SCAR3.SA', 'SHUL4.SA', 'SLCE3.SA', 'SLED4.SA', 'SMLS3.SA',
            'SOND5.SA', 'SULA3.SA', 'TAEE4.SA', 'TEKA4.SA', 'TELB4.SA', 'TEND3.SA',
            'TGMA3.SA', 'TIMP3.SA', 'TKNO4.SA', 'TOTS3.SA', 'TOYB4.SA', 'TRPL4.SA',
            'UGPA3.SA', 'UNIP3.SA', 'USIM3.SA', 'VALE5.SA', 'VCPA4.SA', 'VIVR3.SA',
            'VULC3.SA', 'WLMM4.SA', 'WIZS3.SA', 'YDUQ3.SA'
        ]
        
        # Lista das principais ações do Ibovespa (para análise rápida) - Atualizada sem ações removidas
        self.ibovespa_stocks = [
            'PETR4.SA', 'VALE3.SA', 'ITUB4.SA', 'BBDC4.SA', 'ABEV3.SA',
            'WEGE3.SA', 'RENT3.SA', 'LREN3.SA', 'MGLU3.SA', 'B3SA3.SA',
            'JBSS3.SA', 'SUZB3.SA', 'RAIL3.SA', 'GGBR4.SA', 'BBAS3.SA',
            'ELET3.SA', 'SANB11.SA', 'CSNA3.SA', 'USIM5.SA', 'BRAP4.SA'
        ]
        
        # Fundos Imobiliários (FIIs) - Lista completa do IFIX (117 fundos)
        self.real_estate_funds = [
            "CACR11.SA", "AFHI11.SA", "AJFI11.SA", "ALZR11.SA", "RZAT11.SA", "FATN11.SA", 
            "ARRI11.SA", "AIEC11.SA", "BARI11.SA", "BBIG11.SA", "BRCR11.SA", "BCIA11.SA", 
            "BCRI11.SA", "BLMG11.SA", "BRCO11.SA", "BROF11.SA", "BTAL11.SA", "BTCI11.SA", 
            "BPML11.SA", "BTHF11.SA", "BTLG11.SA", "CCME11.SA", "CPTS11.SA", "ICRI11.SA", 
            "CLIN11.SA", "CPSH11.SA", "CVBI11.SA", "CYCR11.SA", "DEVA11.SA", "VRTA11.SA", 
            "GTWR11.SA", "GZIT11.SA", "GGRC11.SA", "GARE11.SA", "HABT11.SA", "HCTR11.SA", 
            "HGBS11.SA", "HGCR11.SA", "HGFF11.SA", "HGLG11.SA", "HGPO11.SA", "HGRE11.SA", 
            "HGRU11.SA", "HTMX11.SA", "HSAF11.SA", "HSLG11.SA", "HSML11.SA", "HFOF11.SA", 
            "IRDM11.SA", "ITRI11.SA", "JSAF11.SA", "JSRE11.SA", "KISU11.SA", "KNRI11.SA", 
            "KCRE11.SA", "KNHF11.SA", "KNHY11.SA", "KNIP11.SA", "KNCR11.SA", "KNSC11.SA", 
            "KNUQ11.SA", "KFOF11.SA", "KIVO11.SA", "KORE11.SA", "LIFE11.SA", "LVBI11.SA", 
            "MALL11.SA", "MANA11.SA", "MCCI11.SA", "MCRE11.SA", "MXRF11.SA", "MFII11.SA", 
            "OUJP11.SA", "PATL11.SA", "PMIS11.SA", "PORD11.SA", "PVBI11.SA", "RBRL11.SA", 
            "RBRX11.SA", "RBRY11.SA", "RBRP11.SA", "RBRF11.SA", "RBRR11.SA", "RECR11.SA", 
            "RBFF11.SA", "RCRB11.SA", "RBVA11.SA", "RZAK11.SA", "RZTR11.SA", "RVBI11.SA", 
            "SARE11.SA", "TRBL11.SA", "SPXS11.SA", "SNCI11.SA", "SNEL11.SA", "SNFF11.SA", 
            "TEPP11.SA", "TGAR11.SA", "TVRI11.SA", "TOPP11.SA", "TRXF11.SA", "URPR11.SA", 
            "VGHF11.SA", "VGIP11.SA", "VGIR11.SA", "VCJR11.SA", "VGRI11.SA", "VIUR11.SA", 
            "VILG11.SA", "VINO11.SA", "VISC11.SA", "VRTM11.SA", "WHGR11.SA", "XPCI11.SA", 
            "XPLG11.SA", "XPML11.SA", "XPSF11.SA"
        ]
        
        # Fundos de Investimento em Cadeias Produtivas Agroindustriais
        self.agro_funds = [
            'FIAG11.SA', 'AGRO11.SA', 'RBBV11.SA', 'SOJA11.SA', 'BEEF11.SA',
            'CORN11.SA', 'FAIR11.SA', 'SCPF11.SA', 'FOFT11.SA', 'LFTT11.SA',
            'PATC11.SA', 'GTWR11.SA', 'TEPP11.SA', 'SADI11.SA', 'VRTA11.SA',
            'RFOF11.SA', 'FCFL11.SA', 'RBFF11.SA', 'KDIF11.SA', 'RBRD11.SA'
        ]

    def clean_stock_lists(self):
        """Remove ações que foram identificadas como problemáticas"""
        problematic_stocks = []
        
        # Lista de ações conhecidas como removidas ou problemáticas
        known_problematic = ['CIEL3.SA', 'OIBR3.SA', 'OIBR4.SA']
        
        # Remover da lista do Ibovespa
        self.ibovespa_stocks = [stock for stock in self.ibovespa_stocks if stock not in known_problematic]
        
        # Remover da lista completa da B3
        self.b3_stocks = [stock for stock in self.b3_stocks if stock not in known_problematic]
        
        return len(known_problematic)

    def get_stock_data(self, symbols, period="1y"):
        """Coleta dados das ações com otimização para grandes volumes e cache"""
        data = {}
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        successful_downloads = 0
        failed_downloads = 0
        cached_loads = 0
        
        # Criar chave de cache baseada nos símbolos e período
        cache_key = f"{len(symbols)}_{period}_{hash(tuple(sorted(symbols)))}"
        
        for i, symbol in enumerate(symbols):
            try:
                status_text.text(f"Analisando {symbol.replace('.SA', '')} ({i+1}/{len(symbols)})")
                
                # Verificar cache primeiro
                symbol_cache_key = f"{symbol}_{period}"
                if symbol_cache_key in st.session_state.data_cache:
                    data[symbol] = st.session_state.data_cache[symbol_cache_key]
                    cached_loads += 1
                else:
                    stock = yf.Ticker(symbol)
                    
                    # Tentar obter dados históricos com timeout
                    try:
                        hist = stock.history(period=period, timeout=10)
                    except Exception as download_error:
                        if "delisted" in str(download_error).lower() or "no data found" in str(download_error).lower():
                            # Ação pode ter sido removida da bolsa
                            pass
                        failed_downloads += 1
                        continue
                    
                    # Tentar obter informações da empresa
                    try:
                        info = stock.info if hasattr(stock, 'info') else {}
                    except:
                        info = {}
                    
                    if not hist.empty and len(hist) > 5:  # Mínimo de 5 dias de dados
                        try:
                            stock_data = {
                                'history': hist,
                                'info': info,
                                'current_price': hist['Close'].iloc[-1],
                                'price_change': ((hist['Close'].iloc[-1] / hist['Close'].iloc[0]) - 1) * 100,
                                'volatility': hist['Close'].pct_change().std() * np.sqrt(252) * 100,
                                'volume_avg': hist['Volume'].mean()
                            }
                            data[symbol] = stock_data
                            # Salvar no cache
                            st.session_state.data_cache[symbol_cache_key] = stock_data
                            successful_downloads += 1
                        except Exception as calc_error:
                            failed_downloads += 1
                            continue
                    else:
                        failed_downloads += 1
                
                progress_bar.progress((i + 1) / len(symbols))
                
                # Delay adaptativo baseado no número de símbolos
                if i < len(symbols) - 1:  # Não fazer delay no último
                    if len(symbols) > 100:
                        time.sleep(0.02)  # Delay muito pequeno para análises grandes
                    elif len(symbols) > 50:
                        time.sleep(0.03)  # Delay pequeno
                    else:
                        time.sleep(0.05)  # Delay normal
                
            except Exception as e:
                failed_downloads += 1
                # Só mostrar warning se muitos falharem
                if failed_downloads <= 3:  # Mostrar apenas os primeiros 3 erros
                    error_msg = str(e)
                    if "delisted" in error_msg.lower():
                        st.info(f"📋 {symbol.replace('.SA', '')} pode ter sido removido da bolsa")
                    elif "no data found" in error_msg.lower():
                        st.info(f"📋 Sem dados disponíveis para {symbol.replace('.SA', '')}")
                    else:
                        st.warning(f"⚠️ Erro ao carregar {symbol.replace('.SA', '')}: {error_msg[:50]}...")
                continue
        
        progress_bar.empty()
        status_text.empty()
        
        if cached_loads > 0:
            st.success(f"✅ Análise concluída: {successful_downloads} novos downloads, {cached_loads} do cache, {failed_downloads} falharam")
        elif failed_downloads > 0:
            st.info(f"📊 Análise concluída: {successful_downloads} ativos carregados com sucesso, {failed_downloads} falharam")
            if failed_downloads > 5:
                st.warning("⚠️ Muitas falhas detectadas. Algumas ações podem ter sido removidas da bolsa ou estar com problemas temporários.")
        else:
            st.success(f"✅ Análise concluída: {successful_downloads} ativos carregados com sucesso!")
        
        return data

    def calculate_metrics(self, data):
        """Calcula métricas de análise com tratamento melhorado de dados"""
        metrics = []
        
        for symbol, stock_data in data.items():
            try:
                info = stock_data['info']
                hist = stock_data['history']
                
                # Calcula métricas técnicas
                ma_20 = hist['Close'].rolling(20).mean().iloc[-1] if len(hist) >= 20 else hist['Close'].mean()
                ma_50 = hist['Close'].rolling(50).mean().iloc[-1] if len(hist) >= 50 else hist['Close'].mean()
                current_price = stock_data['current_price']
                
                # Score baseado em múltiplos indicadores
                score = 0
                
                # Tendência de preço (30%)
                if stock_data['price_change'] > 0:
                    score += 30
                
                # Posição relativa às médias móveis (25%)
                if current_price > ma_20:
                    score += 12.5
                if current_price > ma_50:
                    score += 12.5
                
                # Volatilidade (20% - menor volatilidade = melhor)
                if stock_data['volatility'] < 30:
                    score += 20
                elif stock_data['volatility'] < 50:
                    score += 10
                
                # Volume (15%)
                if stock_data['volume_avg'] > 1000000:
                    score += 15
                elif stock_data['volume_avg'] > 500000:
                    score += 7.5
                
                # P/L Ratio (10%) - com tratamento de erros
                pe_ratio = None
                try:
                    pe_ratio = info.get('trailingPE', None)
                    if pe_ratio and isinstance(pe_ratio, (int, float)) and pe_ratio > 0:
                        if 10 < pe_ratio < 20:
                            score += 10
                        elif pe_ratio < 30:
                            score += 5
                    else:
                        pe_ratio = None
                except:
                    pe_ratio = None
                
                # Converter P/L para string consistente
                pe_display = f"{pe_ratio:.2f}" if pe_ratio and pe_ratio > 0 else "N/A"
                
                metrics.append({
                    'Symbol': symbol.replace('.SA', ''),
                    'Preço Atual': f"R$ {current_price:.2f}",
                    'Variação (%)': f"{stock_data['price_change']:.2f}%",
                    'Volatilidade (%)': f"{stock_data['volatility']:.2f}%",
                    'P/L': pe_display,
                    'Volume Médio': f"{stock_data['volume_avg']:.0f}",
                    'Score': round(score, 1),
                    'MA20': ma_20,
                    'MA50': ma_50,
                    'raw_data': stock_data
                })
                
            except Exception as e:
                st.warning(f"Erro ao calcular métricas para {symbol}: {str(e)}")
                continue
        
        if not metrics:
            return pd.DataFrame()
            
        df = pd.DataFrame(metrics).sort_values('Score', ascending=False)
        return df

    def create_recommendation_chart(self, df, title):
        """Cria gráfico de recomendações"""
        top_10 = df.head(10)
        
        fig = go.Figure()
        
        # Gráfico de barras com cores baseadas no score
        colors = ['#2e7d32' if score >= 70 else '#ff9800' if score >= 50 else '#f44336' 
                 for score in top_10['Score']]
        
        fig.add_trace(go.Bar(
            x=top_10['Symbol'],
            y=top_10['Score'],
            text=top_10['Score'],
            textposition='auto',
            marker_color=colors,
            name='Score de Recomendação'
        ))
        
        fig.update_layout(
            title=dict(text=title, x=0.5, font=dict(size=20, color='#2e7d32')),
            xaxis_title="Ativo",
            yaxis_title="Score",
            template="plotly_white",
            height=500,
            showlegend=False
        )
        
        return fig

    def create_performance_chart(self, data, symbols):
        """Cria gráfico de performance comparativa com tratamento de erros"""
        fig = go.Figure()
        
        # Filtrar símbolos que têm dados válidos
        valid_symbols = []
        for symbol in symbols[:5]:  # Top 5 para não poluir o gráfico
            # Verificar se o símbolo já tem .SA ou precisa adicionar
            symbol_key = symbol + '.SA' if not symbol.endswith('.SA') else symbol
            
            if symbol_key in data:
                try:
                    hist = data[symbol_key]['history']
                    if not hist.empty and len(hist) > 5:
                        valid_symbols.append((symbol, symbol_key))
                except:
                    continue
        
        if not valid_symbols:
            # Se não há dados válidos, criar gráfico vazio com mensagem
            fig.add_annotation(
                text="Não há dados suficientes para mostrar performance comparativa",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                showarrow=False,
                font=dict(size=16, color="gray")
            )
        else:
            # Cores para cada linha
            colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
            
            for i, (display_symbol, data_key) in enumerate(valid_symbols):
                try:
                    hist = data[data_key]['history']
                    
                    # Calcular retorno percentual
                    returns = (hist['Close'] / hist['Close'].iloc[0] - 1) * 100
                    
                    fig.add_trace(go.Scatter(
                        x=hist.index,
                        y=returns,
                        mode='lines',
                        name=display_symbol.replace('.SA', ''),
                        line=dict(width=2, color=colors[i % len(colors)]),
                        hovertemplate='<b>%{fullData.name}</b><br>' +
                                    'Data: %{x}<br>' +
                                    'Retorno: %{y:.2f}%<br>' +
                                    '<extra></extra>'
                    ))
                except Exception as e:
                    continue
        
        fig.update_layout(
            title=dict(text="Performance Comparativa (Últimos 12 Meses)", 
                      x=0.5, font=dict(size=20, color='#2e7d32')),
            xaxis_title="Data",
            yaxis_title="Retorno (%)",
            template="plotly_white",
            height=500,
            hovermode='x unified',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        return fig

def main():
    st.markdown('<h1 class="main-header">📈 Análise de Investimentos Brasil</h1>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <p style="font-size: 1.2rem; color: #666;">
            Sistema completo de análise para 390+ ações da B3, 117 FIIs do IFIX e Fundos Agroindustriais
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    analyzer = InvestmentAnalyzer()
    
    # Limpar listas de ações problemáticas
    cleaned_count = analyzer.clean_stock_lists()
    if cleaned_count > 0:
        st.sidebar.info(f"🧹 {cleaned_count} ações problemáticas removidas automaticamente")
    
    # Sidebar
    st.sidebar.header("🔧 Configurações")
    
    analysis_type = st.sidebar.selectbox(
        "Tipo de Análise:",
        ["Ações do Ibovespa", "Todas as Ações da B3", "Fundos Imobiliários (FIIs)", "Fundos Agroindustriais", "Análise Completa"]
    )
    
    period = st.sidebar.selectbox(
        "Período de Análise:",
        ["6mo", "1y", "2y", "5y"],
        index=1
    )
    
    num_fiis = st.sidebar.selectbox(
        "Número de FIIs para analisar:",
        [20, 30, 50, "Todos (117)"],
        index=1,
        help="Mais FIIs = análise mais completa, mas demora mais tempo"
    )
    
    num_stocks = st.sidebar.selectbox(
        "Número de ações B3 para analisar:",
        [30, 50, 100, 200, "Todas (390+)"],
        index=1,
        help="Mais ações = análise mais completa, mas demora mais tempo"
    )
    
    if st.sidebar.button("🚀 Iniciar Análise", type="primary"):
        # Aviso sobre tempo de análise
        if (num_fiis == "Todos (117)" or num_fiis >= 50 or 
            num_stocks == "Todas (390+)" or num_stocks >= 100):
            st.warning("⏱️ Análise completa pode levar vários minutos. Por favor, aguarde...")
        
        with st.spinner("Coletando e analisando dados..."):
            
            if analysis_type == "Ações do Ibovespa":
                data = analyzer.get_stock_data(analyzer.ibovespa_stocks, period)
                df = analyzer.calculate_metrics(data)
                
                st.subheader("📊 Melhores Ações do Ibovespa")
                
            elif analysis_type == "Todas as Ações da B3":
                stocks_to_analyze = len(analyzer.b3_stocks) if num_stocks == "Todas (390+)" else num_stocks
                data = analyzer.get_stock_data(analyzer.b3_stocks[:stocks_to_analyze], period)
                df = analyzer.calculate_metrics(data)
                
                st.subheader(f"📊 Melhores Ações da B3 (Analisando {stocks_to_analyze}/{len(analyzer.b3_stocks)} ações)")
                
            elif analysis_type == "Fundos Imobiliários (FIIs)":
                fiis_to_analyze = len(analyzer.real_estate_funds) if num_fiis == "Todos (117)" else num_fiis
                data = analyzer.get_stock_data(analyzer.real_estate_funds[:fiis_to_analyze], period)
                df = analyzer.calculate_metrics(data)
                
                st.subheader(f"🏢 Melhores Fundos Imobiliários (Analisando {fiis_to_analyze}/{len(analyzer.real_estate_funds)} FIIs)")
                
            elif analysis_type == "Fundos Agroindustriais":
                data = analyzer.get_stock_data(analyzer.agro_funds, period)
                df = analyzer.calculate_metrics(data)
                
                st.subheader("🌾 Melhores Fundos Agroindustriais")
                
            else:  # Análise Completa
                st.subheader("📈 Análise Completa de Investimentos")
                
                # Análise de Ações
                st.markdown("### 🔥 Top Ações do Ibovespa")
                stocks_data = analyzer.get_stock_data(analyzer.ibovespa_stocks, period)
                stocks_df = analyzer.calculate_metrics(stocks_data)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.plotly_chart(analyzer.create_recommendation_chart(
                        stocks_df, "Top Ações por Score"), use_container_width=True, key="stocks_recommendation")
                with col2:
                    st.plotly_chart(analyzer.create_performance_chart(
                        stocks_data, stocks_df['Symbol'].tolist()), use_container_width=True, key="stocks_performance")
                
                # Análise Adicional de Ações B3
                st.markdown("### 📈 Top Ações da B3 (Análise Expandida)")
                stocks_b3_to_analyze = min(50, len(analyzer.b3_stocks))  # Usar 50 ações para análise completa
                stocks_b3_data = analyzer.get_stock_data(analyzer.b3_stocks[:stocks_b3_to_analyze], period)
                stocks_b3_df = analyzer.calculate_metrics(stocks_b3_data)
                
                st.info(f"📊 Analisando {stocks_b3_to_analyze} de {len(analyzer.b3_stocks)} ações da B3")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.plotly_chart(analyzer.create_recommendation_chart(
                        stocks_b3_df, "Top Ações B3 por Score"), use_container_width=True, key="stocks_b3_recommendation")
                with col2:
                    st.plotly_chart(analyzer.create_performance_chart(
                        stocks_b3_data, stocks_b3_df['Symbol'].tolist()), use_container_width=True, key="stocks_b3_performance")
                
                # Análise de FIIs
                st.markdown(f"### 🏢 Top Fundos Imobiliários")
                fiis_to_analyze = len(analyzer.real_estate_funds) if num_fiis == "Todos (117)" else num_fiis
                fiis_data = analyzer.get_stock_data(analyzer.real_estate_funds[:fiis_to_analyze], period)
                fiis_df = analyzer.calculate_metrics(fiis_data)
                
                st.info(f"📊 Analisando {fiis_to_analyze} de {len(analyzer.real_estate_funds)} FIIs disponíveis no IFIX")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.plotly_chart(analyzer.create_recommendation_chart(
                        fiis_df, "Top FIIs por Score"), use_container_width=True, key="fiis_recommendation")
                with col2:
                    st.plotly_chart(analyzer.create_performance_chart(
                        fiis_data, fiis_df['Symbol'].tolist()), use_container_width=True, key="fiis_performance")
                
                # Análise de Fundos Agro
                st.markdown("### 🌾 Top Fundos Agroindustriais")
                agro_data = analyzer.get_stock_data(analyzer.agro_funds[:10], period)
                agro_df = analyzer.calculate_metrics(agro_data)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.plotly_chart(analyzer.create_recommendation_chart(
                        agro_df, "Top Fundos Agro por Score"), use_container_width=True, key="agro_recommendation")
                with col2:
                    st.plotly_chart(analyzer.create_performance_chart(
                        agro_data, agro_df['Symbol'].tolist()), use_container_width=True, key="agro_performance")
                
                # Resumo Executivo
                st.markdown("### 🎯 Resumo Executivo - Melhores Oportunidades")
                
                best_stock = stocks_df.iloc[0] if not stocks_df.empty else None
                best_stock_b3 = stocks_b3_df.iloc[0] if not stocks_b3_df.empty else None
                best_fii = fiis_df.iloc[0] if not fiis_df.empty else None
                best_agro = agro_df.iloc[0] if not agro_df.empty else None
                
                col1, col2, col3, col4 = st.columns(4)
                
                if best_stock is not None:
                    with col1:
                        st.markdown(f"""
                        <div class="recommendation-card">
                            <h4>🥇 Melhor Ibovespa</h4>
                            <h2>{best_stock['Symbol']}</h2>
                            <p><strong>Score:</strong> {best_stock['Score']}/100</p>
                            <p><strong>Preço:</strong> {best_stock['Preço Atual']}</p>
                            <p><strong>Variação:</strong> {best_stock['Variação (%)']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                
                if best_stock_b3 is not None:
                    with col2:
                        st.markdown(f"""
                        <div class="recommendation-card">
                            <h4>🚀 Melhor B3</h4>
                            <h2>{best_stock_b3['Symbol']}</h2>
                            <p><strong>Score:</strong> {best_stock_b3['Score']}/100</p>
                            <p><strong>Preço:</strong> {best_stock_b3['Preço Atual']}</p>
                            <p><strong>Variação:</strong> {best_stock_b3['Variação (%)']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                
                if best_fii is not None:
                    with col3:
                        st.markdown(f"""
                        <div class="recommendation-card">
                            <h4>🏢 Melhor FII</h4>
                            <h2>{best_fii['Symbol']}</h2>
                            <p><strong>Score:</strong> {best_fii['Score']}/100</p>
                            <p><strong>Preço:</strong> {best_fii['Preço Atual']}</p>
                            <p><strong>Variação:</strong> {best_fii['Variação (%)']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                
                if best_agro is not None:
                    with col4:
                        st.markdown(f"""
                        <div class="recommendation-card">
                            <h4>🌾 Melhor Fundo Agro</h4>
                            <h2>{best_agro['Symbol']}</h2>
                            <p><strong>Score:</strong> {best_agro['Score']}/100</p>
                            <p><strong>Preço:</strong> {best_agro['Preço Atual']}</p>
                            <p><strong>Variação:</strong> {best_agro['Variação (%)']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                
                return
            
            if not df.empty:
                # Exibir métricas principais
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    avg_score = df['Score'].mean()
                    st.metric("Score Médio", f"{avg_score:.1f}", 
                             delta=f"{avg_score-50:.1f} vs benchmark")
                
                with col2:
                    positive_returns = (df['Variação (%)'].str.replace('%', '').astype(float) > 0).sum()
                    st.metric("Ativos em Alta", f"{positive_returns}/{len(df)}")
                
                with col3:
                    best_performer = df.iloc[0]['Symbol']
                    st.metric("Melhor Ativo", best_performer)
                
                with col4:
                    top_score = df.iloc[0]['Score']
                    st.metric("Maior Score", f"{top_score:.1f}")
                
                # Gráficos
                col1, col2 = st.columns(2)
                
                with col1:
                    fig1 = analyzer.create_recommendation_chart(df, "Ranking por Score")
                    st.plotly_chart(fig1, use_container_width=True, key="individual_recommendation")
                
                with col2:
                    fig2 = analyzer.create_performance_chart(data, df['Symbol'].tolist())
                    st.plotly_chart(fig2, use_container_width=True, key="individual_performance")
                
                # Tabela detalhada
                st.subheader("📋 Análise Detalhada")
                
                # Preparar dados para exibição - garantir compatibilidade com Arrow
                display_df = df[['Symbol', 'Preço Atual', 'Variação (%)', 
                               'Volatilidade (%)', 'P/L', 'Score']].copy()
                
                # Garantir que todos os tipos são compatíveis com Arrow
                display_df['Score'] = display_df['Score'].astype(float)
                display_df = display_df.fillna('N/A')  # Substituir valores nulos
                
                # Colorir linhas baseado no score
                def highlight_score(row):
                    try:
                        score = float(row['Score'])
                        if score >= 70:
                            return ['background-color: #e8f5e8'] * len(row)
                        elif score >= 50:
                            return ['background-color: #fff3e0'] * len(row)
                        else:
                            return ['background-color: #ffebee'] * len(row)
                    except:
                        return ['background-color: #f5f5f5'] * len(row)
                
                try:
                    styled_df = display_df.style.apply(highlight_score, axis=1)
                    st.dataframe(styled_df, use_container_width=True)
                except Exception as e:
                    # Se falhar com estilo, mostrar sem formatação
                    st.dataframe(display_df, use_container_width=True)
                    st.warning(f"⚠️ Formatação de cores não disponível: {str(e)}")
                
                # Recomendações específicas
                st.subheader("💡 Recomendações Baseadas em IA")
                
                top_3 = df.head(3)
                
                for i, (_, row) in enumerate(top_3.iterrows(), 1):
                    score = row['Score']
                    symbol = row['Symbol']
                    price_change = float(row['Variação (%)'].replace('%', ''))
                    
                    if score >= 70:
                        recommendation = "COMPRA FORTE"
                        color = "#2e7d32"
                        justification = f"Score elevado ({score:.1f}), boa performance ({price_change:.1f}%) e baixa volatilidade."
                    elif score >= 50:
                        recommendation = "COMPRA MODERADA"
                        color = "#ff9800"
                        justification = f"Score razoável ({score:.1f}), mas requer acompanhamento da volatilidade."
                    else:
                        recommendation = "AGUARDAR"
                        color = "#f44336"
                        justification = f"Score baixo ({score:.1f}), sugere-se aguardar melhores condições."
                    
                    st.markdown(f"""
                    <div style="border-left: 4px solid {color}; padding: 1rem; margin: 1rem 0; background: #f8f9fa;">
                        <h4 style="color: {color}; margin: 0;">#{i} - {symbol}</h4>
                        <p style="margin: 0.5rem 0;"><strong>Recomendação:</strong> <span style="color: {color};">{recommendation}</span></p>
                        <p style="margin: 0; color: #666;">{justification}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            else:
                st.error("Não foi possível carregar dados suficientes para análise.")
    
    # Botão para limpar cache
    if st.sidebar.button("🗑️ Limpar Cache", help="Remove dados em cache para forçar download atualizado"):
        st.session_state.data_cache = {}
        st.sidebar.success("Cache limpo! Próximas análises usarão dados atualizados.")
            
        if analysis_type == "Ações do Ibovespa":
            data = analyzer.get_stock_data(analyzer.ibovespa_stocks, period)
            df = analyzer.calculate_metrics(data)
            
            st.subheader("📊 Melhores Ações do Ibovespa")
            
        elif analysis_type == "Todas as Ações da B3":
            stocks_to_analyze = len(analyzer.b3_stocks) if num_stocks == "Todas (400+)" else num_stocks
            data = analyzer.get_stock_data(analyzer.b3_stocks[:stocks_to_analyze], period)
            df = analyzer.calculate_metrics(data)
            
            st.subheader(f"📊 Melhores Ações da B3 (Analisando {stocks_to_analyze}/{len(analyzer.b3_stocks)} ações)")
            
        elif analysis_type == "Fundos Imobiliários (FIIs)":
            fiis_to_analyze = len(analyzer.real_estate_funds) if num_fiis == "Todos (117)" else num_fiis
            data = analyzer.get_stock_data(analyzer.real_estate_funds[:fiis_to_analyze], period)
            df = analyzer.calculate_metrics(data)
            
            st.subheader(f"🏢 Melhores Fundos Imobiliários (Analisando {fiis_to_analyze}/{len(analyzer.real_estate_funds)} FIIs)")
            
        elif analysis_type == "Fundos Agroindustriais":
            data = analyzer.get_stock_data(analyzer.agro_funds, period)
            df = analyzer.calculate_metrics(data)
            
            st.subheader("🌾 Melhores Fundos Agroindustriais")
            
        else:  # Análise Completa
            st.subheader("📈 Análise Completa de Investimentos")
            
            # Análise de Ações
            st.markdown("### 🔥 Top Ações do Ibovespa")
            stocks_data = analyzer.get_stock_data(analyzer.ibovespa_stocks[:10], period)
            stocks_df = analyzer.calculate_metrics(stocks_data)
            
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(analyzer.create_recommendation_chart(
                    stocks_df, "Top Ações por Score"), use_container_width=True, key="stocks_recommendation")
            with col2:
                st.plotly_chart(analyzer.create_performance_chart(
                    stocks_data, stocks_df['Symbol'].tolist()), use_container_width=True, key="stocks_performance")
            
            # Análise de FIIs
            st.markdown(f"### 🏢 Top Fundos Imobiliários")
            fiis_to_analyze = len(analyzer.real_estate_funds) if num_fiis == "Todos (117)" else num_fiis
            fiis_data = analyzer.get_stock_data(analyzer.real_estate_funds[:fiis_to_analyze], period)
            fiis_df = analyzer.calculate_metrics(fiis_data)
            
            st.info(f"📊 Analisando {fiis_to_analyze} de {len(analyzer.real_estate_funds)} FIIs disponíveis no IFIX")
            
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(analyzer.create_recommendation_chart(
                    fiis_df, "Top FIIs por Score"), use_container_width=True, key="fiis_recommendation")
            with col2:
                st.plotly_chart(analyzer.create_performance_chart(
                    fiis_data, fiis_df['Symbol'].tolist()), use_container_width=True, key="fiis_performance")
            
            # Análise de Fundos Agro
            st.markdown("### 🌾 Top Fundos Agroindustriais")
            agro_data = analyzer.get_stock_data(analyzer.agro_funds[:10], period)
            agro_df = analyzer.calculate_metrics(agro_data)
            
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(analyzer.create_recommendation_chart(
                    agro_df, "Top Fundos Agro por Score"), use_container_width=True, key="agro_recommendation")
            with col2:
                st.plotly_chart(analyzer.create_performance_chart(
                    agro_data, agro_df['Symbol'].tolist()), use_container_width=True, key="agro_performance")
            
            # Resumo Executivo
            st.markdown("### 🎯 Resumo Executivo - Melhores Oportunidades")
            
            best_stock = stocks_df.iloc[0] if not stocks_df.empty else None
            best_stock_b3 = stocks_b3_df.iloc[0] if not stocks_b3_df.empty else None
            best_fii = fiis_df.iloc[0] if not fiis_df.empty else None
            best_agro = agro_df.iloc[0] if not agro_df.empty else None
            
            col1, col2, col3, col4 = st.columns(4)
            
            if best_stock is not None:
                with col1:
                    st.markdown(f"""
                    <div class="recommendation-card">
                        <h4>🥇 Melhor Ibovespa</h4>
                        <h2>{best_stock['Symbol']}</h2>
                        <p><strong>Score:</strong> {best_stock['Score']}/100</p>
                        <p><strong>Preço:</strong> {best_stock['Preço Atual']}</p>
                        <p><strong>Variação:</strong> {best_stock['Variação (%)']}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            if best_stock_b3 is not None:
                with col2:
                    st.markdown(f"""
                    <div class="recommendation-card">
                        <h4>🚀 Melhor B3</h4>
                        <h2>{best_stock_b3['Symbol']}</h2>
                        <p><strong>Score:</strong> {best_stock_b3['Score']}/100</p>
                        <p><strong>Preço:</strong> {best_stock_b3['Preço Atual']}</p>
                        <p><strong>Variação:</strong> {best_stock_b3['Variação (%)']}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            if best_fii is not None:
                with col3:
                    st.markdown(f"""
                    <div class="recommendation-card">
                        <h4>🏢 Melhor FII</h4>
                        <h2>{best_fii['Symbol']}</h2>
                        <p><strong>Score:</strong> {best_fii['Score']}/100</p>
                        <p><strong>Preço:</strong> {best_fii['Preço Atual']}</p>
                        <p><strong>Variação:</strong> {best_fii['Variação (%)']}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            if best_agro is not None:
                with col4:
                    st.markdown(f"""
                    <div class="recommendation-card">
                        <h4>🌾 Melhor Fundo Agro</h4>
                        <h2>{best_agro['Symbol']}</h2>
                        <p><strong>Score:</strong> {best_agro['Score']}/100</p>
                        <p><strong>Preço:</strong> {best_agro['Preço Atual']}</p>
                        <p><strong>Variação:</strong> {best_agro['Variação (%)']}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            return
        
        if not df.empty:
            # Exibir métricas principais
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                avg_score = df['Score'].mean()
                st.metric("Score Médio", f"{avg_score:.1f}", 
                            delta=f"{avg_score-50:.1f} vs benchmark")
            
            with col2:
                positive_returns = (df['Variação (%)'].str.replace('%', '').astype(float) > 0).sum()
                st.metric("Ativos em Alta", f"{positive_returns}/{len(df)}")
            
            with col3:
                best_performer = df.iloc[0]['Symbol']
                st.metric("Melhor Ativo", best_performer)
            
            with col4:
                top_score = df.iloc[0]['Score']
                st.metric("Maior Score", f"{top_score:.1f}")
            
            # Gráficos
            col1, col2 = st.columns(2)
            
            with col1:
                fig1 = analyzer.create_recommendation_chart(df, "Ranking por Score")
                st.plotly_chart(fig1, use_container_width=True, key="individual_recommendation")
            
            with col2:
                fig2 = analyzer.create_performance_chart(data, df['Symbol'].tolist())
                st.plotly_chart(fig2, use_container_width=True, key="individual_performance")
            
            # Tabela detalhada
            st.subheader("📋 Análise Detalhada")
            
            # Colorir linhas baseado no score
            def highlight_score(row):
                if row['Score'] >= 70:
                    return ['background-color: #e8f5e8'] * len(row)
                elif row['Score'] >= 50:
                    return ['background-color: #fff3e0'] * len(row)
                else:
                    return ['background-color: #ffebee'] * len(row)
            
            styled_df = df[['Symbol', 'Preço Atual', 'Variação (%)', 
                            'Volatilidade (%)', 'P/L', 'Score']].style.apply(highlight_score, axis=1)
            
            st.dataframe(styled_df, use_container_width=True)
            
            # Recomendações específicas
            st.subheader("💡 Recomendações Baseadas em IA")
            
            top_3 = df.head(3)
            
            for i, (_, row) in enumerate(top_3.iterrows(), 1):
                score = row['Score']
                symbol = row['Symbol']
                price_change = float(row['Variação (%)'].replace('%', ''))
                
                if score >= 70:
                    recommendation = "COMPRA FORTE"
                    color = "#2e7d32"
                    justification = f"Score elevado ({score:.1f}), boa performance ({price_change:.1f}%) e baixa volatilidade."
                elif score >= 50:
                    recommendation = "COMPRA MODERADA"
                    color = "#ff9800"
                    justification = f"Score razoável ({score:.1f}), mas requer acompanhamento da volatilidade."
                else:
                    recommendation = "AGUARDAR"
                    color = "#f44336"
                    justification = f"Score baixo ({score:.1f}), sugere-se aguardar melhores condições."
                
                st.markdown(f"""
                <div style="border-left: 4px solid {color}; padding: 1rem; margin: 1rem 0; background: #f8f9fa;">
                    <h4 style="color: {color}; margin: 0;">#{i} - {symbol}</h4>
                    <p style="margin: 0.5rem 0;"><strong>Recomendação:</strong> <span style="color: {color};">{recommendation}</span></p>
                    <p style="margin: 0; color: #666;">{justification}</p>
                </div>
                """, unsafe_allow_html=True)
        
        else:
            st.error("Não foi possível carregar dados suficientes para análise.")
    
    # Informações adicionais
    with st.expander("ℹ️ Metodologia de Análise"):
        st.markdown("""
        ### Como funciona nosso Score de Recomendação:
        
        **Componentes do Score (0-100 pontos):**
        - 📈 **Tendência de Preço (30%):** Performance no período analisado
        - 📊 **Análise Técnica (25%):** Posição relativa às médias móveis (20 e 50 períodos)
        - 📉 **Volatilidade (20%):** Menor volatilidade indica maior estabilidade
        - 💰 **Liquidez (15%):** Volume médio de negociação
        - 📋 **Múltiplos (10%):** P/L e outros indicadores fundamentalistas
        
        **Interpretação:**
        - 🟢 **70-100:** Compra Forte
        - 🟡 **50-69:** Compra Moderada  
        - 🔴 **0-49:** Aguardar melhores condições
        
        ### 📊 Dados dos FIIs:
        - **Fonte:** Lista oficial do IFIX (Índice de Fundos de Investimento Imobiliário)
        - **Total:** 117 fundos imobiliários ativos
        - **Atualização:** Dados de 01/07/2025
        
        ### 📈 Dados das Ações B3:
        - **Fonte:** Ações listadas na B3 (Brasil, Bolsa, Balcão)
        - **Total:** 390+ ações de diversos segmentos (filtradas automaticamente)
        - **Segmentos:** Petróleo, Mineração, Bancos, Varejo, Tecnologia, Energia, Construção, Agronegócio e mais
        
        ### ⚡ Otimizações de Performance:
        - **Cache inteligente:** Dados ficam em cache durante a sessão
        - **Download otimizado:** Timeout de 10s por ativo
        - **Delay adaptativo:** Menor delay para análises grandes
        - **Progress tracking:** Acompanhe o progresso em tempo real
        - **Filtro automático:** Remove ações sem dados ou removidas da bolsa
        
        ### 🔧 Tratamento de Erros:
        - **Ações removidas:** Automaticamente identificadas e ignoradas
        - **Dados incompletos:** Filtrados para garantir qualidade
        - **Compatibilidade Arrow:** Tratamento especial para exibição de tabelas
        """)
    
    # Mostrar status do cache na sidebar
    cache_size = len(st.session_state.get('data_cache', {}))
    if cache_size > 0:
        st.sidebar.info(f"💾 Cache: {cache_size} ativos salvos\n⚡ Próximas análises serão mais rápidas!")
    else:
        st.sidebar.info("💾 Cache vazio\n⏱️ Primeira análise pode demorar mais")
    
    with st.expander("📋 Lista Completa de FIIs Analisados"):
        st.markdown("### 🏢 117 Fundos Imobiliários do IFIX:")
        
        # Mostrar fundos em colunas organizadas
        fundos_clean = [fundo.replace('.SA', '') for fundo in analyzer.real_estate_funds]
        
        # Dividir em 6 colunas
        cols = st.columns(6)
        for i, fundo in enumerate(fundos_clean):
            with cols[i % 6]:
                st.text(fundo)
    
    with st.expander("📈 Lista de Ações da B3 por Segmento"):
        st.markdown("### 🏭 400+ Ações da B3 por Segmento:")
        
        # Organizar por segmentos (primeiros de cada categoria)
        segmentos = {
            "🛢️ Petróleo & Gás": ["PETR3", "PETR4", "PRIO3", "RRRP3", "RECV3", "3R11"],
            "⛏️ Mineração": ["VALE3", "CSNA3", "GGBR4", "USIM5", "GOAU4", "FESA4"],
            "🏦 Bancos": ["ITUB4", "BBDC4", "BBAS3", "SANB11", "BPAC11", "BMGB4"],
            "🛒 Varejo": ["MGLU3", "LREN3", "AMER3", "PCAR3", "VVAR3", "GUAR3"],
            "🍺 Alimentos & Bebidas": ["ABEV3", "JBSS3", "BRFS3", "MRFG3", "SMLS3", "CAML3"],
            "💻 Tecnologia": ["VIVT3", "TIMS3", "DESK3", "TOTS3", "IFCM3", "LWSA3"],
            "⚡ Energia": ["ELET3", "EQTL3", "CPFE3", "CMIG4", "CPLE6", "TAEE11"],
            "🏗️ Construção": ["MRVE3", "CYRE3", "EVEN3", "GFSA3", "JHSF3", "HBTS5"],
            "🌱 Agronegócio": ["SLC3", "TERA3", "SOJA3", "LAND3", "RUMO3", "RAIZ4"],
            "🚛 Transporte": ["RAIL3", "CCRO3", "LOGN3", "AZUL4", "GOLL4", "EMBR3"]
        }
        
        for segmento, acoes in segmentos.items():
            st.markdown(f"**{segmento}:**")
            st.text(", ".join(acoes) + " e mais...")
            
        st.info("💡 Esta é apenas uma amostra. O sistema inclui 390+ ações de todos os segmentos da B3!")
        
        # Mostrar total de ações por categoria
        total_acoes = len(analyzer.b3_stocks)
        total_fiis = len(analyzer.real_estate_funds)
        total_agro = len(analyzer.agro_funds)
        
        st.markdown(f"""
        ### 📊 Resumo dos Ativos Disponíveis:
        - 📈 **Ações B3:** {total_acoes} empresas
        - 🏢 **FIIs:** {total_fiis} fundos imobiliários  
        - 🌾 **Fundos Agro:** {total_agro} fundos agroindustriais
        - 🎯 **Total:** {total_acoes + total_fiis + total_agro} ativos para análise
        """)
    
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: #666;'>💼 Sistema de Análise de Investimentos Brasil | "
        "390+ Ações B3 + 117 FIIs + Fundos Agro | Desenvolvido com IA para otimizar seus investimentos</p>", 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()