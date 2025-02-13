import pandas as pd
import plotly.express as px
import random 
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
from dash import Dash,html,dcc,Input,Output
import datetime
import math
import os

d1 = pd.read_excel('Vendas.xlsx')
d2 = pd.read_excel('Vendas - Dez.xlsx')

# dia da semana
def dia(a,m,d):
    """recebe o ano, mês e dia de uma data
    e retorna o nome do dia da semana"""
    sem = ("Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo")
    num = datetime.date(a, m, d).weekday()
    return sem[num]
# d1
d1['Data']=pd.to_datetime(d1['Data'])
d1['Ano']=d1['Data'].dt.year
d1['Mês']=d1['Data'].dt.month
d1['Dia']=d1['Data'].dt.day
for ind in list(d1.index):
    d1.loc[ind,'Dia da semana']=dia(d1.loc[ind,'Ano'], d1.loc[ind,'Mês'], d1.loc[ind,'Dia'])
# d2
d2['Data']=pd.to_datetime(d2['Data'])
d2['Ano']=d2['Data'].dt.year
d2['Mês']=d2['Data'].dt.month
d2['Dia']=d2['Data'].dt.day
for ind in list(d2.index):
    d2.loc[ind,'Dia da semana']=dia(d2.loc[ind,'Ano'], d2.loc[ind,'Mês'], d2.loc[ind,'Dia'])

# sexo do comprador
hm=['Homem','Homem','Mulher']
for c in list(d1.index):
    d1.loc[c,'Sexo']=random.choice(hm)
for c in list(d2.index):
    d2.loc[c,'Sexo']=random.choice(hm)
    
# idade do comprador
idades=[]
for c in range(0,20000):
    idades.append(random.randint(18,25))
for c in range(0,40000):
    idades.append(random.randint(26,35))
for c in range(0,20000):
    idades.append(random.randint(36,45))
for c in range(0,13910):
    idades.append(random.randint(46,65))
for c in range(0,93910):
    d1.loc[c,'Idade']= random.choice(idades)
for c in range(0,7089):
    d2.loc[c,'Idade']= random.choice(idades)
# metodos de pagamento
pag = ['Pix','Crédito','Débito','Dinheiro']
for c in range(0,93910):
    d1.loc[c,'Pagamento']=random.choice(pag)
for c in range(0,7089):
    d2.loc[c,'Pagamento']=random.choice(pag)
# custo
for c in range(0,93910):
    n = random.randint(10,60)
    d1.loc[c,'Custo']=d1.loc[c,'Valor Unitário']*(n/100)
for c in range(0,7089):
    n = random.randint(10,60)
    d2.loc[c,'Custo']=d2.loc[c,'Valor Unitário']*(n/100)

dados = pd.concat([d1,d2], axis=0)
# data
dados['Data']=pd.to_datetime(dados['Data'])
dados['Mês']=dados['Data'].dt.month
# lucro
dados['Lucro']=dados['Valor Final']-(dados['Custo']*dados['Quantidade'])

lojas = ['Shopping Vila Velha','Norte Shopping','Iguatemi Campinas','Salvador Shopping','Bourbon Shopping SP']
dados.rename(columns={'ID Loja':'Loja'}, inplace=True)
vendasinit = dados.query('Loja in ["Shopping Vila Velha","Norte Shopping","Iguatemi Campinas","Salvador Shopping","Bourbon Shopping SP"]')
vendas = vendasinit.query('Mês == 2 and Dia in [1,2,3,4,5,6,7]')

# FAT E LUC 

# SEMANAL
fat = vendas[['Dia','Valor Final','Lucro']].groupby('Dia').sum()
for i in list(fat.index):
    fat.loc[i,'Dia']=i
fat.rename(columns={'Valor Final':'Faturamento'}, inplace=True)
fattot = fat['Faturamento'].sum()
luctot = fat['Lucro'].sum()

fl7 = px.bar(fat, x='Dia', y=['Faturamento','Lucro'], barmode='group', color_discrete_map={'Faturamento':'darkcyan','Lucro':'cyan'}, template='plotly_dark',
            labels={'value':'Valor em R$'}, title=f'Faturamento total = R${fattot} / Lucro total = R${luctot:.0f}')
# QUINZENA
vds15 = vendasinit.query('Mês == 2 and Dia in [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]')
fat15 = vds15[['Dia','Valor Final','Lucro']].groupby('Dia').sum()
for i in list(fat15.index):
    fat15.loc[i,'Dia']=i
fat15.rename(columns={'Valor Final':'Faturamento'}, inplace=True)
fattot15 = fat15['Faturamento'].sum()
luctot15 = fat15['Lucro'].sum()

fl15 = px.bar(fat15, x='Dia', y=['Faturamento','Lucro'], barmode='group', color_discrete_map={'Faturamento':'darkcyan','Lucro':'cyan'}, template='plotly_dark',
            labels={'value':'Valor em R$'}, title=f'Faturamento total = R${fattot15} / Lucro total = R${luctot15:.0f}')
# MENSAL
vds30 = vendasinit.query('Mês == 2')
fat30 = vds30[['Dia','Valor Final','Lucro']].groupby('Dia').sum()
for i in list(fat30.index):
    fat30.loc[i,'Dia']=i
fat30.rename(columns={'Valor Final':'Faturamento'}, inplace=True)
fattot30 = fat30['Faturamento'].sum()
luctot30 = fat30['Lucro'].sum()

fl30 = px.bar(fat30, x='Dia', y=['Faturamento','Lucro'], barmode='group', color_discrete_map={'Faturamento':'darkcyan','Lucro':'cyan'}, template='plotly_dark',
            labels={'value':'Valor em R$'}, title=f'Faturamento total = R${fattot30} / Lucro total = R${luctot30:.0f}')

# ANUAL 
fatano = vendasinit[['Mês','Valor Final','Lucro']].groupby('Mês').sum()
for i in list(fatano.index):
    fatano.loc[i,'Mês']=i
fatano.rename(columns={'Valor Final':'Faturamento'}, inplace=True)
fattot = fatano['Faturamento'].sum()
luctot = fatano['Lucro'].sum()

flano = px.bar(fatano, x='Mês', y=['Faturamento','Lucro'], barmode='group' ,color_discrete_map={'Faturamento':'darkcyan','Lucro':'cyan'}, template='plotly_dark',
            labels={'value':'Valor em R$'}, title=f'Faturamento total = R${fattot} / Lucro total = R${luctot:.0f}')


# TICKET MÉDIO

# SEMANAL
q = vendas['Dia'].value_counts()
for i in list(fat.index):
    fat.loc[i,'Ticket médio']=fat.loc[i,'Faturamento']/q[i]
ticm = fat['Ticket médio'].mean()
ticxd = px.line(fat, x='Dia', y='Ticket médio', template='plotly_dark', color_discrete_sequence=['yellow'],
               title=f'Ticket médio ao longo da semana (R${ticm:.1f} média)', markers=True)

# QUINZENA
q1 = vds15['Dia'].value_counts()
for i in list(fat15.index):
    fat15.loc[i,'Ticket médio']=fat15.loc[i,'Faturamento']/q1[i]
ticm15 = fat15['Ticket médio'].mean()
ticxd15 = px.line(fat15, x='Dia', y='Ticket médio', template='plotly_dark',
                  color_discrete_sequence=['yellow'],
                  title=f'Ticket médio ao longo da quinzena (R${ticm15:.1f} média)', markers=True)

# MENSAL
q2 = vds30['Dia'].value_counts()
for i in list(fat30.index):
    fat30.loc[i,'Ticket médio']=fat30.loc[i,'Faturamento']/q2[i]
ticm30 = fat30['Ticket médio'].mean()
ticxd30 = px.line(fat30, x='Dia', y='Ticket médio', template='plotly_dark',
                  color_discrete_sequence=['yellow'],
                  title=f'Ticket médio ao longo do mês (R${ticm30:.1f} média)', markers=True)

# ANUAL 
q3 = vendasinit['Mês'].value_counts()
fatmes = vendasinit[['Mês','Valor Final']].groupby('Mês').sum()
fatmes.rename(columns={'Valor Final':'Faturamento'}, inplace=True)
for i in list(fatmes.index):
    fatmes.loc[i,'Mês']=i
for i in list(fatmes.index):
    fatmes.loc[i,'Ticket médio']=fatmes.loc[i,'Faturamento']/q3[i]
ticmano = fatmes['Ticket médio'].mean()
ticxdano = px.line(fatmes, x='Mês', y='Ticket médio', template='plotly_dark',
                  color_discrete_sequence=['yellow'],
                  title=f'Ticket médio ao longo do ano (R${ticmano:.1f} média)', markers=True)
# quantidade vendida de cada produto por categoria

# SEMANAL
quant = vendas[['Produto','Quantidade']].groupby('Produto').sum()
ber = []
cal = []
cam = []
for n in list(quant.index):
    quant.loc[n,'Produto']=n
    if 'Bermuda' in n:
        ber.append(n)
    if 'Calça' in n:
        cal.append(n)
    if 'Camisa' in n:
        cam.append(n)
comp3 = make_subplots(rows=2, cols=3, specs=[[{'rowspan':2,'type':'bar'}, {'rowspan':2,'type':'bar'}, {'rowspan':2,'type':'bar'}],
                                                 [None, None, None]],
                                               subplot_titles=('Bermudas','Calças','Camisas'))
comp3.update_annotations(font_size=20)
comp3.update_layout(template='plotly_dark')
bermuda = quant.query(f"Produto in {ber}")
calça = quant.query(f"Produto in {cal}")
camisa = quant.query(f"Produto in {cam}")
comp3.add_trace(go.Bar(x=bermuda['Produto'], y=bermuda['Quantidade'], marker=dict(color='lightcyan'), name='Bermudas'), row=1, col=1)
comp3.add_trace(go.Bar(x=calça['Produto'], y=calça['Quantidade'], marker=dict(color='cyan'), name='Calças'), row=1, col=2)
comp3.add_trace(go.Bar(x=camisa['Produto'], y=camisa['Quantidade'], marker=dict(color='royalblue'), name='Camisas'), row=1, col=3)
comp3.update_yaxes(title_text='Quantidade vendida', row=1, col=1)
    

cams = []
casa = []
chin = []
for n in list(quant.index):
    quant.loc[n,'Produto']=n
    if 'Camiseta' in n:
        cams.append(n)
    if 'Casaco' in n:
        casa.append(n)
    if 'Chinelo' in n:
        chin.append(n)
comp6 = make_subplots(rows=2, cols=3, specs=[[{'rowspan':2,'type':'bar'}, {'rowspan':2,'type':'bar'}, {'rowspan':2,'type':'bar'}],
                                                [None, None, None]],
                                                subplot_titles=('Camisetas','Casacos','Chinelos'))
comp6.update_annotations(font_size=20)
comp6.update_layout(template='plotly_dark')
camiseta = quant.query(f"Produto in {cams}")
casaco = quant.query(f"Produto in {casa}")
chinelo = quant.query(f"Produto in {chin}")
comp6.add_trace(go.Bar(x=camiseta['Produto'], y=camiseta['Quantidade'], marker=dict(color='lightcyan'), name='Camisetas'), row=1, col=1)
comp6.add_trace(go.Bar(x=casaco['Produto'], y=casaco['Quantidade'], marker=dict(color='cyan'), name='Casacos'), row=1, col=2)
comp6.add_trace(go.Bar(x=chinelo['Produto'], y=chinelo['Quantidade'], marker=dict(color='royalblue'), name='Chinelos'), row=1, col=3)
comp6.update_yaxes(title_text='Quantidade vendida', row=1, col=1)


cint = []
cuec = []
gor = []
for n in list(quant.index):
    quant.loc[n,'Produto']=n
    if 'Cinto' in n:
        cint.append(n)
    if 'Cueca' in n:
        cuec.append(n)
    if 'Gorro' in n:
        gor.append(n)
comp9 = make_subplots(rows=2, cols=3, specs=[[{'rowspan':2,'type':'bar'}, {'rowspan':2,'type':'bar'}, {'rowspan':2,'type':'bar'}],
                                             [None, None, None]],
                                           subplot_titles=('Cintos','Cuecas','Gorros'))
comp9.update_annotations(font_size=20)
comp9.update_layout(template='plotly_dark')
cinto = quant.query(f"Produto in {cint}")
cueca = quant.query(f"Produto in {cuec}")
gorro = quant.query(f"Produto in {gor}")
comp9.add_trace(go.Bar(x=cinto['Produto'], y=cinto['Quantidade'], marker=dict(color='lightcyan'), name='Cintos'), row=1, col=1)
comp9.add_trace(go.Bar(x=cueca['Produto'], y=cueca['Quantidade'], marker=dict(color='cyan'), name='Cuecas'), row=1, col=2)
comp9.add_trace(go.Bar(x=gorro['Produto'], y=gorro['Quantidade'], marker=dict(color='royalblue'), name='Gorros'), row=1, col=3)
comp9.update_yaxes(title_text='Quantidade vendida', row=1, col=1)
    

mei = []
moch = []
pol = []
for n in list(quant.index):
    quant.loc[n,'Produto']=n
    if 'Meia' in n:
        mei.append(n)
    if 'Mochila' in n:
        moch.append(n)
    if 'Polo' in n:
        pol.append(n)
comp12 = make_subplots(rows=2, cols=3, specs=[[{'rowspan':2,'type':'bar'}, {'rowspan':2,'type':'bar'}, {'rowspan':2,'type':'bar'}],
                                             [None, None, None]],
                                           subplot_titles=('Meias','Mochilas','Polos'))
comp12.update_annotations(font_size=20)
comp12.update_layout(template='plotly_dark')
meia = quant.query(f"Produto in {mei}")
mochila = quant.query(f"Produto in {moch}")
polo = quant.query(f"Produto in {pol}")
comp12.add_trace(go.Bar(x=meia['Produto'], y=meia['Quantidade'], marker=dict(color='lightcyan'), name='Meias'), row=1, col=1)
comp12.add_trace(go.Bar(x=mochila['Produto'], y=mochila['Quantidade'], marker=dict(color='cyan'), name='Mochilas'), row=1, col=2)
comp12.add_trace(go.Bar(x=polo['Produto'], y=polo['Quantidade'], marker=dict(color='royalblue'), name='Polos'), row=1, col=3)
comp12.update_yaxes(title_text='Quantidade vendida', row=1, col=1)


puls = []
rel = []
sap = []
for n in list(quant.index):
    quant.loc[n,'Produto']=n
    if 'Pulseira' in n:
        puls.append(n)
    if 'Relógio' in n:
        rel.append(n)
    if 'Sapato' in n:
        sap.append(n)
comp15 = make_subplots(rows=2, cols=3, specs=[[{'rowspan':2,'type':'bar'}, {'rowspan':2,'type':'bar'}, {'rowspan':2,'type':'bar'}],
                                             [None, None, None]],
                                           subplot_titles=('Pulseiras','Relógios','Sapatos'))
comp15.update_annotations(font_size=20)
comp15.update_layout(template='plotly_dark')
pulseira = quant.query(f"Produto in {puls}")
relogio = quant.query(f"Produto in {rel}")
sapato = quant.query(f"Produto in {sap}")
comp15.add_trace(go.Bar(x=pulseira['Produto'], y=pulseira['Quantidade'], marker=dict(color='lightcyan'), name='Pulseiras'), row=1, col=1)
comp15.add_trace(go.Bar(x=relogio['Produto'], y=relogio['Quantidade'], marker=dict(color='cyan'), name='Relógios'), row=1, col=2)
comp15.add_trace(go.Bar(x=sapato['Produto'], y=sapato['Quantidade'], marker=dict(color='royalblue'), name='Sapatos'), row=1, col=3)
comp15.update_yaxes(title_text='Quantidade vendida', row=1, col=1)
    


sho = []
sung = []
ter = []
for n in list(quant.index):
    quant.loc[n,'Produto']=n
    if 'Short' in n:
        sho.append(n)
    if 'Sunga' in n:
        sung.append(n)
    if 'Terno' in n:
        ter.append(n)
comp18 = make_subplots(rows=2, cols=3, specs=[[{'rowspan':2,'type':'bar'}, {'rowspan':2,'type':'bar'}, {'rowspan':2,'type':'bar'}],
                                             [None, None, None]],
                                           subplot_titles=('Shorts','Sungas','Ternos'))
comp18.update_annotations(font_size=20)
comp18.update_layout(template='plotly_dark')
short = quant.query(f"Produto in {sho}")
sunga = quant.query(f"Produto in {sung}")
terno = quant.query(f"Produto in {ter}")
comp18.add_trace(go.Bar(x=short['Produto'], y=short['Quantidade'], marker=dict(color='lightcyan'), name='Shorts'), row=1, col=1)
comp18.add_trace(go.Bar(x=sunga['Produto'], y=sunga['Quantidade'], marker=dict(color='cyan'), name='Sungas'), row=1, col=2)
comp18.add_trace(go.Bar(x=terno['Produto'], y=terno['Quantidade'], marker=dict(color='royalblue'), name='Ternos'), row=1, col=3)
comp18.update_yaxes(title_text='Quantidade vendida', row=1, col=1)
    


teni = []
for n in list(quant.index):
    quant.loc[n,'Produto']=n
    if 'Tênis' in n:
        teni.append(n)
comp21 = make_subplots(rows=2, cols=3, specs=[[{'rowspan':2, 'colspan':2,'type':'bar'}, None, {'rowspan':2, 'type':'domain'}],
                                             [None, None, None]],
                                           subplot_titles=('Tênis','Quantidade de vendas X Gênero'))
comp21.update_annotations(font_size=20)
comp21.update_layout(template='plotly_dark')
tenis = quant.query(f"Produto in {teni}")
piem = vendas['Sexo'].value_counts()['Mulher']
pieh = vendas['Sexo'].value_counts()['Homem']
comp21Py = [] 
comp21Py.append(pieh) 
comp21Py.append(piem)
comp21.add_trace(go.Bar(x=tenis['Produto'], y=tenis['Quantidade'], marker=dict(color='darkcyan'), name='Tênis'), row=1, col=1)
comp21.update_yaxes(title_text='Quantidade vendida', row=1, col=1)
comp21.add_trace(go.Pie(labels=['Homem','Mulher'], values=comp21Py, marker=dict(colors=('cyan','red'))), row=1, col=3)
    


# QUINZENA
quant = vds15[['Produto','Quantidade']].groupby('Produto').sum()
ber = []
cal = []
cam = []
for n in list(quant.index):
    quant.loc[n,'Produto']=n
    if 'Bermuda' in n:
        ber.append(n)
    if 'Calça' in n:
        cal.append(n)
    if 'Camisa' in n:
        cam.append(n)
comp315 = make_subplots(rows=2, cols=3, specs=[[{'rowspan':2,'type':'bar'}, {'rowspan':2,'type':'bar'}, {'rowspan':2,'type':'bar'}],
                                                 [None, None, None]],
                                               subplot_titles=('Bermudas','Calças','Camisas'))
comp315.update_annotations(font_size=20)
comp315.update_layout(template='plotly_dark')
bermuda = quant.query(f"Produto in {ber}")
calça = quant.query(f"Produto in {cal}")
camisa = quant.query(f"Produto in {cam}")
comp315.add_trace(go.Bar(x=bermuda['Produto'], y=bermuda['Quantidade'], marker=dict(color='lightcyan'), name='Bermudas'), row=1, col=1)
comp315.add_trace(go.Bar(x=calça['Produto'], y=calça['Quantidade'], marker=dict(color='cyan'), name='Calças'), row=1, col=2)
comp315.add_trace(go.Bar(x=camisa['Produto'], y=camisa['Quantidade'], marker=dict(color='royalblue'), name='Camisas'), row=1, col=3)
comp315.update_yaxes(title_text='Quantidade vendida', row=1, col=1)

cams = []
casa = []
chin = []
for n in list(quant.index):
    quant.loc[n,'Produto']=n
    if 'Camiseta' in n:
        cams.append(n)
    if 'Casaco' in n:
        casa.append(n)
    if 'Chinelo' in n:
        chin.append(n)
comp615 = make_subplots(rows=2, cols=3, specs=[[{'rowspan':2,'type':'bar'}, {'rowspan':2,'type':'bar'}, {'rowspan':2,'type':'bar'}],
                                                [None, None, None]],
                                                subplot_titles=('Camisetas','Casacos','Chinelos'))
comp615.update_annotations(font_size=20)
comp615.update_layout(template='plotly_dark')
camiseta = quant.query(f"Produto in {cams}")
casaco = quant.query(f"Produto in {casa}")
chinelo = quant.query(f"Produto in {chin}")
comp615.add_trace(go.Bar(x=camiseta['Produto'], y=camiseta['Quantidade'], marker=dict(color='lightcyan'), name='Camisetas'), row=1, col=1)
comp615.add_trace(go.Bar(x=casaco['Produto'], y=casaco['Quantidade'], marker=dict(color='cyan'), name='Casacos'), row=1, col=2)
comp615.add_trace(go.Bar(x=chinelo['Produto'], y=chinelo['Quantidade'], marker=dict(color='royalblue'), name='Chinelos'), row=1, col=3)
comp615.update_yaxes(title_text='Quantidade vendida', row=1, col=1)

cint = []
cuec = []
gor = []
for n in list(quant.index):
    quant.loc[n,'Produto']=n
    if 'Cinto' in n:
        cint.append(n)
    if 'Cueca' in n:
        cuec.append(n)
    if 'Gorro' in n:
        gor.append(n)
comp915 = make_subplots(rows=2, cols=3, specs=[[{'rowspan':2,'type':'bar'}, {'rowspan':2,'type':'bar'}, {'rowspan':2,'type':'bar'}],
                                             [None, None, None]],
                                           subplot_titles=('Cintos','Cuecas','Gorros'))
comp915.update_annotations(font_size=20)
comp915.update_layout(template='plotly_dark')
cinto = quant.query(f"Produto in {cint}")
cueca = quant.query(f"Produto in {cuec}")
gorro = quant.query(f"Produto in {gor}")
comp915.add_trace(go.Bar(x=cinto['Produto'], y=cinto['Quantidade'], marker=dict(color='lightcyan'), name='Cintos'), row=1, col=1)
comp915.add_trace(go.Bar(x=cueca['Produto'], y=cueca['Quantidade'], marker=dict(color='cyan'), name='Cuecas'), row=1, col=2)
comp915.add_trace(go.Bar(x=gorro['Produto'], y=gorro['Quantidade'], marker=dict(color='royalblue'), name='Gorros'), row=1, col=3)
comp915.update_yaxes(title_text='Quantidade vendida', row=1, col=1)


mei = []
moch = []
pol = []
for n in list(quant.index):
    quant.loc[n,'Produto']=n
    if 'Meia' in n:
        mei.append(n)
    if 'Mochila' in n:
        moch.append(n)
    if 'Polo' in n:
        pol.append(n)
comp1215 = make_subplots(rows=2, cols=3, specs=[[{'rowspan':2,'type':'bar'}, {'rowspan':2,'type':'bar'}, {'rowspan':2,'type':'bar'}],
                                             [None, None, None]],
                                           subplot_titles=('Meias','Mochilas','Polos'))
comp1215.update_annotations(font_size=20)
comp1215.update_layout(template='plotly_dark')
meia = quant.query(f"Produto in {mei}")
mochila = quant.query(f"Produto in {moch}")
polo = quant.query(f"Produto in {pol}")
comp1215.add_trace(go.Bar(x=meia['Produto'], y=meia['Quantidade'], marker=dict(color='lightcyan'), name='Meias'), row=1, col=1)
comp1215.add_trace(go.Bar(x=mochila['Produto'], y=mochila['Quantidade'], marker=dict(color='cyan'), name='Mochilas'), row=1, col=2)
comp1215.add_trace(go.Bar(x=polo['Produto'], y=polo['Quantidade'], marker=dict(color='royalblue'), name='Polos'), row=1, col=3)
comp1215.update_yaxes(title_text='Quantidade vendida', row=1, col=1)

puls = []
rel = []
sap = []
for n in list(quant.index):
    quant.loc[n,'Produto']=n
    if 'Pulseira' in n:
        puls.append(n)
    if 'Relógio' in n:
        rel.append(n)
    if 'Sapato' in n:
        sap.append(n)
comp1515 = make_subplots(rows=2, cols=3, specs=[[{'rowspan':2,'type':'bar'}, {'rowspan':2,'type':'bar'}, {'rowspan':2,'type':'bar'}],
                                             [None, None, None]],
                                           subplot_titles=('Pulseiras','Relógios','Sapatos'))
comp1515.update_annotations(font_size=20)
comp1515.update_layout(template='plotly_dark')
pulseira = quant.query(f"Produto in {puls}")
relogio = quant.query(f"Produto in {rel}")
sapato = quant.query(f"Produto in {sap}")
comp1515.add_trace(go.Bar(x=pulseira['Produto'], y=pulseira['Quantidade'], marker=dict(color='lightcyan'), name='Pulseiras'), row=1, col=1)
comp1515.add_trace(go.Bar(x=relogio['Produto'], y=relogio['Quantidade'], marker=dict(color='cyan'), name='Relógios'), row=1, col=2)
comp1515.add_trace(go.Bar(x=sapato['Produto'], y=sapato['Quantidade'], marker=dict(color='royalblue'), name='Sapatos'), row=1, col=3)
comp1515.update_yaxes(title_text='Quantidade vendida', row=1, col=1)


sho = []
sung = []
ter = []
for n in list(quant.index):
    quant.loc[n,'Produto']=n
    if 'Short' in n:
        sho.append(n)
    if 'Sunga' in n:
        sung.append(n)
    if 'Terno' in n:
        ter.append(n)
comp1815 = make_subplots(rows=2, cols=3, specs=[[{'rowspan':2,'type':'bar'}, {'rowspan':2,'type':'bar'}, {'rowspan':2,'type':'bar'}],
                                             [None, None, None]],
                                           subplot_titles=('Shorts','Sungas','Ternos'))
comp1815.update_annotations(font_size=20)
comp1815.update_layout(template='plotly_dark')
short = quant.query(f"Produto in {sho}")
sunga = quant.query(f"Produto in {sung}")
terno = quant.query(f"Produto in {ter}")
comp1815.add_trace(go.Bar(x=short['Produto'], y=short['Quantidade'], marker=dict(color='lightcyan'), name='Shorts'), row=1, col=1)
comp1815.add_trace(go.Bar(x=sunga['Produto'], y=sunga['Quantidade'], marker=dict(color='cyan'), name='Sungas'), row=1, col=2)
comp1815.add_trace(go.Bar(x=terno['Produto'], y=terno['Quantidade'], marker=dict(color='royalblue'), name='Ternos'), row=1, col=3)
comp1815.update_yaxes(title_text='Quantidade vendida', row=1, col=1)


teni = []
for n in list(quant.index):
    quant.loc[n,'Produto']=n
    if 'Tênis' in n:
        teni.append(n)
comp2115 = make_subplots(rows=2, cols=3, specs=[[{'rowspan':2, 'colspan':2,'type':'bar'}, None, {'rowspan':2, 'type':'domain'}],
                                             [None, None, None]],
                                           subplot_titles=('Tênis','Quantidade de vendas X Gênero'))
comp2115.update_annotations(font_size=20)
comp2115.update_layout(template='plotly_dark')
tenis = quant.query(f"Produto in {teni}")
piem = vds15['Sexo'].value_counts()['Mulher']
pieh = vds15['Sexo'].value_counts()['Homem']
comp2115Py = [] 
comp2115Py.append(pieh) 
comp2115Py.append(piem)
comp2115.add_trace(go.Bar(x=tenis['Produto'], y=tenis['Quantidade'], marker=dict(color='darkcyan'), name='Tênis'), row=1, col=1)
comp2115.update_yaxes(title_text='Quantidade vendida', row=1, col=1)
comp2115.add_trace(go.Pie(labels=['Homem','Mulher'], values=comp2115Py, marker=dict(colors=('cyan','red'))), row=1, col=3)
    


# MENSAL 
quant = vds30[['Produto','Quantidade']].groupby('Produto').sum()
ber = []
cal = []
cam = []
for n in list(quant.index):
    quant.loc[n,'Produto']=n
    if 'Bermuda' in n:
        ber.append(n)
    if 'Calça' in n:
        cal.append(n)
    if 'Camisa' in n:
        cam.append(n)
comp330 = make_subplots(rows=2, cols=3, specs=[[{'rowspan':2,'type':'bar'}, {'rowspan':2,'type':'bar'}, {'rowspan':2,'type':'bar'}],
                                                 [None, None, None]],
                                               subplot_titles=('Bermudas','Calças','Camisas'))
comp330.update_annotations(font_size=20)
comp330.update_layout(template='plotly_dark')
bermuda = quant.query(f"Produto in {ber}")
calça = quant.query(f"Produto in {cal}")
camisa = quant.query(f"Produto in {cam}")
comp330.add_trace(go.Bar(x=bermuda['Produto'], y=bermuda['Quantidade'], marker=dict(color='lightcyan'), name='Bermudas'), row=1, col=1)
comp330.add_trace(go.Bar(x=calça['Produto'], y=calça['Quantidade'], marker=dict(color='cyan'), name='Calças'), row=1, col=2)
comp330.add_trace(go.Bar(x=camisa['Produto'], y=camisa['Quantidade'], marker=dict(color='royalblue'), name='Camisas'), row=1, col=3)
comp330.update_yaxes(title_text='Quantidade vendida', row=1, col=1)

cams = []
casa = []
chin = []
for n in list(quant.index):
    quant.loc[n,'Produto']=n
    if 'Camiseta' in n:
        cams.append(n)
    if 'Casaco' in n:
        casa.append(n)
    if 'Chinelo' in n:
        chin.append(n)
comp630 = make_subplots(rows=2, cols=3, specs=[[{'rowspan':2,'type':'bar'}, {'rowspan':2,'type':'bar'}, {'rowspan':2,'type':'bar'}],
                                                [None, None, None]],
                                                subplot_titles=('Camisetas','Casacos','Chinelos'))
comp630.update_annotations(font_size=20)
comp630.update_layout(template='plotly_dark')
camiseta = quant.query(f"Produto in {cams}")
casaco = quant.query(f"Produto in {casa}")
chinelo = quant.query(f"Produto in {chin}")
comp630.add_trace(go.Bar(x=camiseta['Produto'], y=camiseta['Quantidade'], marker=dict(color='lightcyan'), name='Camisetas'), row=1, col=1)
comp630.add_trace(go.Bar(x=casaco['Produto'], y=casaco['Quantidade'], marker=dict(color='cyan'), name='Casacos'), row=1, col=2)
comp630.add_trace(go.Bar(x=chinelo['Produto'], y=chinelo['Quantidade'], marker=dict(color='royalblue'), name='Chinelos'), row=1, col=3)
comp630.update_yaxes(title_text='Quantidade vendida', row=1, col=1)

cint = []
cuec = []
gor = []
for n in list(quant.index):
    quant.loc[n,'Produto']=n
    if 'Cinto' in n:
        cint.append(n)
    if 'Cueca' in n:
        cuec.append(n)
    if 'Gorro' in n:
        gor.append(n)
comp930 = make_subplots(rows=2, cols=3, specs=[[{'rowspan':2,'type':'bar'}, {'rowspan':2,'type':'bar'}, {'rowspan':2,'type':'bar'}],
                                             [None, None, None]],
                                           subplot_titles=('Cintos','Cuecas','Gorros'))
comp930.update_annotations(font_size=20)
comp930.update_layout(template='plotly_dark')
cinto = quant.query(f"Produto in {cint}")
cueca = quant.query(f"Produto in {cuec}")
gorro = quant.query(f"Produto in {gor}")
comp930.add_trace(go.Bar(x=cinto['Produto'], y=cinto['Quantidade'], marker=dict(color='lightcyan'), name='Cintos'), row=1, col=1)
comp930.add_trace(go.Bar(x=cueca['Produto'], y=cueca['Quantidade'], marker=dict(color='cyan'), name='Cuecas'), row=1, col=2)
comp930.add_trace(go.Bar(x=gorro['Produto'], y=gorro['Quantidade'], marker=dict(color='royalblue'), name='Gorros'), row=1, col=3)
comp930.update_yaxes(title_text='Quantidade vendida', row=1, col=1)


mei = []
moch = []
pol = []
for n in list(quant.index):
    quant.loc[n,'Produto']=n
    if 'Meia' in n:
        mei.append(n)
    if 'Mochila' in n:
        moch.append(n)
    if 'Polo' in n:
        pol.append(n)
comp1230 = make_subplots(rows=2, cols=3, specs=[[{'rowspan':2,'type':'bar'}, {'rowspan':2,'type':'bar'}, {'rowspan':2,'type':'bar'}],
                                             [None, None, None]],
                                           subplot_titles=('Meias','Mochilas','Polos'))
comp1230.update_annotations(font_size=20)
comp1230.update_layout(template='plotly_dark')
meia = quant.query(f"Produto in {mei}")
mochila = quant.query(f"Produto in {moch}")
polo = quant.query(f"Produto in {pol}")
comp1230.add_trace(go.Bar(x=meia['Produto'], y=meia['Quantidade'], marker=dict(color='lightcyan'), name='Meias'), row=1, col=1)
comp1230.add_trace(go.Bar(x=mochila['Produto'], y=mochila['Quantidade'], marker=dict(color='cyan'), name='Mochilas'), row=1, col=2)
comp1230.add_trace(go.Bar(x=polo['Produto'], y=polo['Quantidade'], marker=dict(color='royalblue'), name='Polos'), row=1, col=3)
comp1230.update_yaxes(title_text='Quantidade vendida', row=1, col=1)

puls = []
rel = []
sap = []
for n in list(quant.index):
    quant.loc[n,'Produto']=n
    if 'Pulseira' in n:
        puls.append(n)
    if 'Relógio' in n:
        rel.append(n)
    if 'Sapato' in n:
        sap.append(n)
comp1530 = make_subplots(rows=2, cols=3, specs=[[{'rowspan':2,'type':'bar'}, {'rowspan':2,'type':'bar'}, {'rowspan':2,'type':'bar'}],
                                             [None, None, None]],
                                           subplot_titles=('Pulseiras','Relógios','Sapatos'))
comp1530.update_annotations(font_size=20)
comp1530.update_layout(template='plotly_dark')
pulseira = quant.query(f"Produto in {puls}")
relogio = quant.query(f"Produto in {rel}")
sapato = quant.query(f"Produto in {sap}")
comp1530.add_trace(go.Bar(x=pulseira['Produto'], y=pulseira['Quantidade'], marker=dict(color='lightcyan'), name='Pulseiras'), row=1, col=1)
comp1530.add_trace(go.Bar(x=relogio['Produto'], y=relogio['Quantidade'], marker=dict(color='cyan'), name='Relógios'), row=1, col=2)
comp1530.add_trace(go.Bar(x=sapato['Produto'], y=sapato['Quantidade'], marker=dict(color='royalblue'), name='Sapatos'), row=1, col=3)
comp1530.update_yaxes(title_text='Quantidade vendida', row=1, col=1)


sho = []
sung = []
ter = []
for n in list(quant.index):
    quant.loc[n,'Produto']=n
    if 'Short' in n:
        sho.append(n)
    if 'Sunga' in n:
        sung.append(n)
    if 'Terno' in n:
        ter.append(n)
comp1830 = make_subplots(rows=2, cols=3, specs=[[{'rowspan':2,'type':'bar'}, {'rowspan':2,'type':'bar'}, {'rowspan':2,'type':'bar'}],
                                             [None, None, None]],
                                           subplot_titles=('Shorts','Sungas','Ternos'))
comp1830.update_annotations(font_size=20)
comp1830.update_layout(template='plotly_dark')
short = quant.query(f"Produto in {sho}")
sunga = quant.query(f"Produto in {sung}")
terno = quant.query(f"Produto in {ter}")
comp1830.add_trace(go.Bar(x=short['Produto'], y=short['Quantidade'], marker=dict(color='lightcyan'), name='Shorts'), row=1, col=1)
comp1830.add_trace(go.Bar(x=sunga['Produto'], y=sunga['Quantidade'], marker=dict(color='cyan'), name='Sungas'), row=1, col=2)
comp1830.add_trace(go.Bar(x=terno['Produto'], y=terno['Quantidade'], marker=dict(color='royalblue'), name='Ternos'), row=1, col=3)
comp1830.update_yaxes(title_text='Quantidade vendida', row=1, col=1)


teni = []
for n in list(quant.index):
    quant.loc[n,'Produto']=n
    if 'Tênis' in n:
        teni.append(n)
comp2130 = make_subplots(rows=2, cols=3, specs=[[{'rowspan':2, 'colspan':2,'type':'bar'}, None, {'rowspan':2, 'type':'domain'}],
                                             [None, None, None]],
                                           subplot_titles=('Tênis','Quantidade de vendas X Gênero'))
comp2130.update_annotations(font_size=20)
comp2130.update_layout(template='plotly_dark')
tenis = quant.query(f"Produto in {teni}")
piem = vds30['Sexo'].value_counts()['Mulher']
pieh = vds30['Sexo'].value_counts()['Homem']
comp2130Py = [] 
comp2130Py.append(pieh) 
comp2130Py.append(piem)
comp2130.add_trace(go.Bar(x=tenis['Produto'], y=tenis['Quantidade'], marker=dict(color='darkcyan'), name='Tênis'), row=1, col=1)
comp2130.update_yaxes(title_text='Quantidade vendida', row=1, col=1)
comp2130.add_trace(go.Pie(labels=['Homem','Mulher'], values=comp2130Py, marker=dict(colors=('cyan','red'))), row=1, col=3)

# ANUAL
quant = vendasinit[['Produto','Quantidade']].groupby('Produto').sum()
ber = []
cal = []
cam = []
for n in list(quant.index):
    quant.loc[n,'Produto']=n
    if 'Bermuda' in n:
        ber.append(n)
    if 'Calça' in n:
        cal.append(n)
    if 'Camisa' in n:
        cam.append(n)
comp3ano = make_subplots(rows=2, cols=3, specs=[[{'rowspan':2,'type':'bar'}, {'rowspan':2,'type':'bar'}, {'rowspan':2,'type':'bar'}],
                                                 [None, None, None]],
                                               subplot_titles=('Bermudas','Calças','Camisas'))
comp3ano.update_annotations(font_size=20)
comp3ano.update_layout(template='plotly_dark')
bermuda = quant.query(f"Produto in {ber}")
calça = quant.query(f"Produto in {cal}")
camisa = quant.query(f"Produto in {cam}")
comp3ano.add_trace(go.Bar(x=bermuda['Produto'], y=bermuda['Quantidade'], marker=dict(color='lightcyan'), name='Bermudas'), row=1, col=1)
comp3ano.add_trace(go.Bar(x=calça['Produto'], y=calça['Quantidade'], marker=dict(color='cyan'), name='Calças'), row=1, col=2)
comp3ano.add_trace(go.Bar(x=camisa['Produto'], y=camisa['Quantidade'], marker=dict(color='royalblue'), name='Camisas'), row=1, col=3)
comp3ano.update_yaxes(title_text='Quantidade vendida', row=1, col=1)

cams = []
casa = []
chin = []
for n in list(quant.index):
    quant.loc[n,'Produto']=n
    if 'Camiseta' in n:
        cams.append(n)
    if 'Casaco' in n:
        casa.append(n)
    if 'Chinelo' in n:
        chin.append(n)
comp6ano = make_subplots(rows=2, cols=3, specs=[[{'rowspan':2,'type':'bar'}, {'rowspan':2,'type':'bar'}, {'rowspan':2,'type':'bar'}],
                                                [None, None, None]],
                                                subplot_titles=('Camisetas','Casacos','Chinelos'))
comp6ano.update_annotations(font_size=20)
comp6ano.update_layout(template='plotly_dark')
camiseta = quant.query(f"Produto in {cams}")
casaco = quant.query(f"Produto in {casa}")
chinelo = quant.query(f"Produto in {chin}")
comp6ano.add_trace(go.Bar(x=camiseta['Produto'], y=camiseta['Quantidade'], marker=dict(color='lightcyan'), name='Camisetas'), row=1, col=1)
comp6ano.add_trace(go.Bar(x=casaco['Produto'], y=casaco['Quantidade'], marker=dict(color='cyan'), name='Casacos'), row=1, col=2)
comp6ano.add_trace(go.Bar(x=chinelo['Produto'], y=chinelo['Quantidade'], marker=dict(color='royalblue'), name='Chinelos'), row=1, col=3)
comp6ano.update_yaxes(title_text='Quantidade vendida', row=1, col=1)


cint = []
cuec = []
gor = []
for n in list(quant.index):
    quant.loc[n,'Produto']=n
    if 'Cinto' in n:
        cint.append(n)
    if 'Cueca' in n:
        cuec.append(n)
    if 'Gorro' in n:
        gor.append(n)
comp9ano = make_subplots(rows=2, cols=3, specs=[[{'rowspan':2,'type':'bar'}, {'rowspan':2,'type':'bar'}, {'rowspan':2,'type':'bar'}],
                                             [None, None, None]],
                                           subplot_titles=('Cintos','Cuecas','Gorros'))
comp9ano.update_annotations(font_size=20)
comp9ano.update_layout(template='plotly_dark')
cinto = quant.query(f"Produto in {cint}")
cueca = quant.query(f"Produto in {cuec}")
gorro = quant.query(f"Produto in {gor}")
comp9ano.add_trace(go.Bar(x=cinto['Produto'], y=cinto['Quantidade'], marker=dict(color='lightcyan'), name='Cintos'), row=1, col=1)
comp9ano.add_trace(go.Bar(x=cueca['Produto'], y=cueca['Quantidade'], marker=dict(color='cyan'), name='Cuecas'), row=1, col=2)
comp9ano.add_trace(go.Bar(x=gorro['Produto'], y=gorro['Quantidade'], marker=dict(color='royalblue'), name='Gorros'), row=1, col=3)
comp9ano.update_yaxes(title_text='Quantidade vendida', row=1, col=1)
mei = []
moch = []
pol = []
for n in list(quant.index):
    quant.loc[n,'Produto']=n
    if 'Meia' in n:
        mei.append(n)
    if 'Mochila' in n:
        moch.append(n)
    if 'Polo' in n:
        pol.append(n)
comp12ano = make_subplots(rows=2, cols=3, specs=[[{'rowspan':2,'type':'bar'}, {'rowspan':2,'type':'bar'}, {'rowspan':2,'type':'bar'}],
                                             [None, None, None]],
                                           subplot_titles=('Meias','Mochilas','Polos'))
comp12ano.update_annotations(font_size=20)
comp12ano.update_layout(template='plotly_dark')
meia = quant.query(f"Produto in {mei}")
mochila = quant.query(f"Produto in {moch}")
polo = quant.query(f"Produto in {pol}")
comp12ano.add_trace(go.Bar(x=meia['Produto'], y=meia['Quantidade'], marker=dict(color='lightcyan'), name='Meias'), row=1, col=1)
comp12ano.add_trace(go.Bar(x=mochila['Produto'], y=mochila['Quantidade'], marker=dict(color='cyan'), name='Mochilas'), row=1, col=2)
comp12ano.add_trace(go.Bar(x=polo['Produto'], y=polo['Quantidade'], marker=dict(color='royalblue'), name='Polos'), row=1, col=3)
comp12ano.update_yaxes(title_text='Quantidade vendida', row=1, col=1)

puls = []
rel = []
sap = []
for n in list(quant.index):
    quant.loc[n,'Produto']=n
    if 'Pulseira' in n:
        puls.append(n)
    if 'Relógio' in n:
        rel.append(n)
    if 'Sapato' in n:
        sap.append(n)
comp15ano = make_subplots(rows=2, cols=3, specs=[[{'rowspan':2,'type':'bar'}, {'rowspan':2,'type':'bar'}, {'rowspan':2,'type':'bar'}],
                                             [None, None, None]],
                                           subplot_titles=('Pulseiras','Relógios','Sapatos'))
comp15ano.update_annotations(font_size=20)
comp15ano.update_layout(template='plotly_dark')
pulseira = quant.query(f"Produto in {puls}")
relogio = quant.query(f"Produto in {rel}")
sapato = quant.query(f"Produto in {sap}")
comp15ano.add_trace(go.Bar(x=pulseira['Produto'], y=pulseira['Quantidade'], marker=dict(color='lightcyan'), name='Pulseiras'), row=1, col=1)
comp15ano.add_trace(go.Bar(x=relogio['Produto'], y=relogio['Quantidade'], marker=dict(color='cyan'), name='Relógios'), row=1, col=2)
comp15ano.add_trace(go.Bar(x=sapato['Produto'], y=sapato['Quantidade'], marker=dict(color='royalblue'), name='Sapatos'), row=1, col=3)
comp15ano.update_yaxes(title_text='Quantidade vendida', row=1, col=1)

sho = []
sung = []
ter = []
for n in list(quant.index):
    quant.loc[n,'Produto']=n
    if 'Short' in n:
        sho.append(n)
    if 'Sunga' in n:
        sung.append(n)
    if 'Terno' in n:
        ter.append(n)
comp18ano = make_subplots(rows=2, cols=3, specs=[[{'rowspan':2,'type':'bar'}, {'rowspan':2,'type':'bar'}, {'rowspan':2,'type':'bar'}],
                                             [None, None, None]],
                                           subplot_titles=('Shorts','Sungas','Ternos'))
comp18ano.update_annotations(font_size=20)
comp18ano.update_layout(template='plotly_dark')
short = quant.query(f"Produto in {sho}")
sunga = quant.query(f"Produto in {sung}")
terno = quant.query(f"Produto in {ter}")
comp18ano.add_trace(go.Bar(x=short['Produto'], y=short['Quantidade'], marker=dict(color='lightcyan'), name='Shorts'), row=1, col=1)
comp18ano.add_trace(go.Bar(x=sunga['Produto'], y=sunga['Quantidade'], marker=dict(color='cyan'), name='Sungas'), row=1, col=2)
comp18ano.add_trace(go.Bar(x=terno['Produto'], y=terno['Quantidade'], marker=dict(color='royalblue'), name='Ternos'), row=1, col=3)
comp18ano.update_yaxes(title_text='Quantidade vendida', row=1, col=1)

teni = []
for n in list(quant.index):
    quant.loc[n,'Produto']=n
    if 'Tênis' in n:
        teni.append(n)
comp21ano = make_subplots(rows=2, cols=3, specs=[[{'rowspan':2, 'colspan':2,'type':'bar'}, None, {'rowspan':2, 'type':'domain'}],
                                             [None, None, None]],
                                           subplot_titles=('Tênis','Quantidade de vendas X Gênero'))
comp21ano.update_annotations(font_size=20)
comp21ano.update_layout(template='plotly_dark')
tenis = quant.query(f"Produto in {teni}")
piem = vendasinit['Sexo'].value_counts()['Mulher']
pieh = vendasinit['Sexo'].value_counts()['Homem']
comp21anoPy = [] 
comp21anoPy.append(pieh) 
comp21anoPy.append(piem)
comp21ano.add_trace(go.Bar(x=tenis['Produto'], y=tenis['Quantidade'], marker=dict(color='darkcyan'), name='Tênis'), row=1, col=1)
comp21ano.update_yaxes(title_text='Quantidade vendida', row=1, col=1)
comp21ano.add_trace(go.Pie(labels=['Homem','Mulher'], values=comp21anoPy, marker=dict(colors=('cyan','red'))), row=1, col=3)
    

# Quantidade de vendas por idade

# SEMANAL
vxi = px.histogram(vendas, x='Idade', color='Sexo', color_discrete_map={'Mulher':'red','Homem':'cyan'}, template='plotly_dark',title='Quantidade de vendas X idade')

# QUINZENA
vxi15 = px.histogram(vds15, x='Idade', color='Sexo', color_discrete_map={'Mulher':'red','Homem':'cyan'}, template='plotly_dark',title='Quantidade de vendas X idade')

# MENSAL
vxi30 = px.histogram(vds30, x='Idade', color='Sexo', color_discrete_map={'Mulher':'red','Homem':'cyan'}, template='plotly_dark',title='Quantidade de vendas X idade')

# ANUAL
vxiano = px.histogram(vendasinit, x='Idade', color='Sexo', color_discrete_map={'Mulher':'red','Homem':'cyan'}, template='plotly_dark',title='Quantidade de vendas X idade')

# quantidade de vendas totais e % por categoria

# SEMANAL
quant = vendas[['Produto','Quantidade']].groupby('Produto').sum()
ber = []
cal = []
cam = []
cams = []
casa = []
chin = []
cint = []
cuec = []
gor = []
mei = []
moch = []
pol = []
puls = []
rel = []
sap = []
sho = []
sung = []
ter = []
teni = []
for n in list(quant.index):
    quant.loc[n,'Produto']=n
    if 'Bermuda' in n:
        ber.append(n)
    if 'Calça' in n:
        cal.append(n)
    if 'Camisa' in n:
        cam.append(n)
    if 'Camiseta' in n:
        cams.append(n)
    if 'Casaco' in n:
        casa.append(n)
    if 'Chinelo' in n:
        chin.append(n)
    if 'Cinto' in n:
        cint.append(n)
    if 'Cueca' in n:
        cuec.append(n)
    if 'Gorro' in n:
        gor.append(n)
    if 'Meia' in n:
        mei.append(n)
    if 'Mochila' in n:
        moch.append(n)
    if 'Polo' in n:
        pol.append(n)
    if 'Pulseira' in n:
        puls.append(n)
    if 'Relógio' in n:
        rel.append(n)
    if 'Sapato' in n:
        sap.append(n)
    if 'Short' in n:
        sho.append(n)
    if 'Sunga' in n:
        sung.append(n)
    if 'Terno' in n:
        ter.append(n)
    if 'Tênis' in n:
        teni.append(n)
bermuda = quant.query(f"Produto in {ber}")
calça = quant.query(f"Produto in {cal}")
camisa = quant.query(f"Produto in {cam}")
camiseta = quant.query(f"Produto in {cams}")
casaco = quant.query(f"Produto in {casa}")
chinelo = quant.query(f"Produto in {chin}")
cinto = quant.query(f"Produto in {cint}")
cueca = quant.query(f"Produto in {cuec}")
gorro = quant.query(f"Produto in {gor}")
meia = quant.query(f"Produto in {mei}")
mochila = quant.query(f"Produto in {moch}")
polo = quant.query(f"Produto in {pol}")
pulseira = quant.query(f"Produto in {puls}")
relogio = quant.query(f"Produto in {rel}")
sapato = quant.query(f"Produto in {sap}")
short = quant.query(f"Produto in {sho}")
sunga = quant.query(f"Produto in {sung}")
terno = quant.query(f"Produto in {ter}")
tenis = quant.query(f"Produto in {teni}")
dic2 = {}
axis1 = ['Bermudas','Calças','Camisas','Camisetas','Casacos','Chinelos','Cintos','Cuecas','Gorros','Meias','Mochilas','Polos','Pulseiras',
        'Relógios','Sapatos','Shorts','Sungas','Ternos','Tênis']
axis2 = []
axis2.append(bermuda['Quantidade'].sum())
axis2.append(calça['Quantidade'].sum())
axis2.append(camisa['Quantidade'].sum())
axis2.append(camiseta['Quantidade'].sum())
axis2.append(casaco['Quantidade'].sum())
axis2.append(chinelo['Quantidade'].sum())
axis2.append(cinto['Quantidade'].sum())
axis2.append(cueca['Quantidade'].sum())
axis2.append(gorro['Quantidade'].sum())
axis2.append(meia['Quantidade'].sum())
axis2.append(mochila['Quantidade'].sum())
axis2.append(polo['Quantidade'].sum())
axis2.append(pulseira['Quantidade'].sum())
axis2.append(relogio['Quantidade'].sum())
axis2.append(sapato['Quantidade'].sum())
axis2.append(short['Quantidade'].sum())
axis2.append(sunga['Quantidade'].sum())
axis2.append(terno['Quantidade'].sum())
axis2.append(tenis['Quantidade'].sum())
dic2['Produtos']=[]
dic2['Quantidade vendida']=[]
for pos,n in enumerate(axis1):
    dic2['Produtos'].append(n)
    dic2['Quantidade vendida'].append(axis2[pos])
dic2df = pd.DataFrame(dic2)
quanttot = dic2df['Quantidade vendida'].sum()
VC = px.pie(dic2df, names='Produtos', values='Quantidade vendida', color='Produtos', template='plotly_dark', hole=0.3, title=f'Quantidade de produtos vendidos por categoria ({quanttot} produtos vendidos)',
           height=500)



# QUINZENA
quant = vds15[['Produto','Quantidade']].groupby('Produto').sum()
ber = []
cal = []
cam = []
cams = []
casa = []
chin = []
cint = []
cuec = []
gor = []
mei = []
moch = []
pol = []
puls = []
rel = []
sap = []
sho = []
sung = []
ter = []
teni = []
for n in list(quant.index):
    quant.loc[n,'Produto']=n
    if 'Bermuda' in n:
        ber.append(n)
    if 'Calça' in n:
        cal.append(n)
    if 'Camisa' in n:
        cam.append(n)
    if 'Camiseta' in n:
        cams.append(n)
    if 'Casaco' in n:
        casa.append(n)
    if 'Chinelo' in n:
        chin.append(n)
    if 'Cinto' in n:
        cint.append(n)
    if 'Cueca' in n:
        cuec.append(n)
    if 'Gorro' in n:
        gor.append(n)
    if 'Meia' in n:
        mei.append(n)
    if 'Mochila' in n:
        moch.append(n)
    if 'Polo' in n:
        pol.append(n)
    if 'Pulseira' in n:
        puls.append(n)
    if 'Relógio' in n:
        rel.append(n)
    if 'Sapato' in n:
        sap.append(n)
    if 'Short' in n:
        sho.append(n)
    if 'Sunga' in n:
        sung.append(n)
    if 'Terno' in n:
        ter.append(n)
    if 'Tênis' in n:
        teni.append(n)
bermuda = quant.query(f"Produto in {ber}")
calça = quant.query(f"Produto in {cal}")
camisa = quant.query(f"Produto in {cam}")
camiseta = quant.query(f"Produto in {cams}")
casaco = quant.query(f"Produto in {casa}")
chinelo = quant.query(f"Produto in {chin}")
cinto = quant.query(f"Produto in {cint}")
cueca = quant.query(f"Produto in {cuec}")
gorro = quant.query(f"Produto in {gor}")
meia = quant.query(f"Produto in {mei}")
mochila = quant.query(f"Produto in {moch}")
polo = quant.query(f"Produto in {pol}")
pulseira = quant.query(f"Produto in {puls}")
relogio = quant.query(f"Produto in {rel}")
sapato = quant.query(f"Produto in {sap}")
short = quant.query(f"Produto in {sho}")
sunga = quant.query(f"Produto in {sung}")
terno = quant.query(f"Produto in {ter}")
tenis = quant.query(f"Produto in {teni}")
dic2 = {}
axis1 = ['Bermudas','Calças','Camisas','Camisetas','Casacos','Chinelos','Cintos','Cuecas','Gorros','Meias','Mochilas','Polos','Pulseiras',
        'Relógios','Sapatos','Shorts','Sungas','Ternos','Tênis']
axis2 = []
axis2.append(bermuda['Quantidade'].sum())
axis2.append(calça['Quantidade'].sum())
axis2.append(camisa['Quantidade'].sum())
axis2.append(camiseta['Quantidade'].sum())
axis2.append(casaco['Quantidade'].sum())
axis2.append(chinelo['Quantidade'].sum())
axis2.append(cinto['Quantidade'].sum())
axis2.append(cueca['Quantidade'].sum())
axis2.append(gorro['Quantidade'].sum())
axis2.append(meia['Quantidade'].sum())
axis2.append(mochila['Quantidade'].sum())
axis2.append(polo['Quantidade'].sum())
axis2.append(pulseira['Quantidade'].sum())
axis2.append(relogio['Quantidade'].sum())
axis2.append(sapato['Quantidade'].sum())
axis2.append(short['Quantidade'].sum())
axis2.append(sunga['Quantidade'].sum())
axis2.append(terno['Quantidade'].sum())
axis2.append(tenis['Quantidade'].sum())
dic2['Produtos']=[]
dic2['Quantidade vendida']=[]
for pos,n in enumerate(axis1):
    dic2['Produtos'].append(n)
    dic2['Quantidade vendida'].append(axis2[pos])
dic2df = pd.DataFrame(dic2)
quanttot = dic2df['Quantidade vendida'].sum()
VC15 = px.pie(dic2df, names='Produtos', values='Quantidade vendida', color='Produtos', template='plotly_dark', hole=0.3, title=f'Quantidade de produtos vendidos por categoria ({quanttot} produtos vendidos)',
           height=500)

# MENSAL
quant = vds30[['Produto','Quantidade']].groupby('Produto').sum()
ber = []
cal = []
cam = []
cams = []
casa = []
chin = []
cint = []
cuec = []
gor = []
mei = []
moch = []
pol = []
puls = []
rel = []
sap = []
sho = []
sung = []
ter = []
teni = []
for n in list(quant.index):
    quant.loc[n,'Produto']=n
    if 'Bermuda' in n:
        ber.append(n)
    if 'Calça' in n:
        cal.append(n)
    if 'Camisa' in n:
        cam.append(n)
    if 'Camiseta' in n:
        cams.append(n)
    if 'Casaco' in n:
        casa.append(n)
    if 'Chinelo' in n:
        chin.append(n)
    if 'Cinto' in n:
        cint.append(n)
    if 'Cueca' in n:
        cuec.append(n)
    if 'Gorro' in n:
        gor.append(n)
    if 'Meia' in n:
        mei.append(n)
    if 'Mochila' in n:
        moch.append(n)
    if 'Polo' in n:
        pol.append(n)
    if 'Pulseira' in n:
        puls.append(n)
    if 'Relógio' in n:
        rel.append(n)
    if 'Sapato' in n:
        sap.append(n)
    if 'Short' in n:
        sho.append(n)
    if 'Sunga' in n:
        sung.append(n)
    if 'Terno' in n:
        ter.append(n)
    if 'Tênis' in n:
        teni.append(n)
bermuda = quant.query(f"Produto in {ber}")
calça = quant.query(f"Produto in {cal}")
camisa = quant.query(f"Produto in {cam}")
camiseta = quant.query(f"Produto in {cams}")
casaco = quant.query(f"Produto in {casa}")
chinelo = quant.query(f"Produto in {chin}")
cinto = quant.query(f"Produto in {cint}")
cueca = quant.query(f"Produto in {cuec}")
gorro = quant.query(f"Produto in {gor}")
meia = quant.query(f"Produto in {mei}")
mochila = quant.query(f"Produto in {moch}")
polo = quant.query(f"Produto in {pol}")
pulseira = quant.query(f"Produto in {puls}")
relogio = quant.query(f"Produto in {rel}")
sapato = quant.query(f"Produto in {sap}")
short = quant.query(f"Produto in {sho}")
sunga = quant.query(f"Produto in {sung}")
terno = quant.query(f"Produto in {ter}")
tenis = quant.query(f"Produto in {teni}")
dic2 = {}
axis1 = ['Bermudas','Calças','Camisas','Camisetas','Casacos','Chinelos','Cintos','Cuecas','Gorros','Meias','Mochilas','Polos','Pulseiras',
        'Relógios','Sapatos','Shorts','Sungas','Ternos','Tênis']
axis2 = []
axis2.append(bermuda['Quantidade'].sum())
axis2.append(calça['Quantidade'].sum())
axis2.append(camisa['Quantidade'].sum())
axis2.append(camiseta['Quantidade'].sum())
axis2.append(casaco['Quantidade'].sum())
axis2.append(chinelo['Quantidade'].sum())
axis2.append(cinto['Quantidade'].sum())
axis2.append(cueca['Quantidade'].sum())
axis2.append(gorro['Quantidade'].sum())
axis2.append(meia['Quantidade'].sum())
axis2.append(mochila['Quantidade'].sum())
axis2.append(polo['Quantidade'].sum())
axis2.append(pulseira['Quantidade'].sum())
axis2.append(relogio['Quantidade'].sum())
axis2.append(sapato['Quantidade'].sum())
axis2.append(short['Quantidade'].sum())
axis2.append(sunga['Quantidade'].sum())
axis2.append(terno['Quantidade'].sum())
axis2.append(tenis['Quantidade'].sum())
dic2['Produtos']=[]
dic2['Quantidade vendida']=[]
for pos,n in enumerate(axis1):
    dic2['Produtos'].append(n)
    dic2['Quantidade vendida'].append(axis2[pos])
dic2df = pd.DataFrame(dic2)
quanttot = dic2df['Quantidade vendida'].sum()
VC30 = px.pie(dic2df, names='Produtos', values='Quantidade vendida', color='Produtos', template='plotly_dark', hole=0.3, title=f'Quantidade de produtos vendidos por categoria ({quanttot} produtos vendidos)',
           height=500)

# ANUAL
quant = vendasinit[['Produto','Quantidade']].groupby('Produto').sum()
ber = []
cal = []
cam = []
cams = []
casa = []
chin = []
cint = []
cuec = []
gor = []
mei = []
moch = []
pol = []
puls = []
rel = []
sap = []
sho = []
sung = []
ter = []
teni = []
for n in list(quant.index):
    quant.loc[n,'Produto']=n
    if 'Bermuda' in n:
        ber.append(n)
    if 'Calça' in n:
        cal.append(n)
    if 'Camisa' in n:
        cam.append(n)
    if 'Camiseta' in n:
        cams.append(n)
    if 'Casaco' in n:
        casa.append(n)
    if 'Chinelo' in n:
        chin.append(n)
    if 'Cinto' in n:
        cint.append(n)
    if 'Cueca' in n:
        cuec.append(n)
    if 'Gorro' in n:
        gor.append(n)
    if 'Meia' in n:
        mei.append(n)
    if 'Mochila' in n:
        moch.append(n)
    if 'Polo' in n:
        pol.append(n)
    if 'Pulseira' in n:
        puls.append(n)
    if 'Relógio' in n:
        rel.append(n)
    if 'Sapato' in n:
        sap.append(n)
    if 'Short' in n:
        sho.append(n)
    if 'Sunga' in n:
        sung.append(n)
    if 'Terno' in n:
        ter.append(n)
    if 'Tênis' in n:
        teni.append(n)
bermuda = quant.query(f"Produto in {ber}")
calça = quant.query(f"Produto in {cal}")
camisa = quant.query(f"Produto in {cam}")
camiseta = quant.query(f"Produto in {cams}")
casaco = quant.query(f"Produto in {casa}")
chinelo = quant.query(f"Produto in {chin}")
cinto = quant.query(f"Produto in {cint}")
cueca = quant.query(f"Produto in {cuec}")
gorro = quant.query(f"Produto in {gor}")
meia = quant.query(f"Produto in {mei}")
mochila = quant.query(f"Produto in {moch}")
polo = quant.query(f"Produto in {pol}")
pulseira = quant.query(f"Produto in {puls}")
relogio = quant.query(f"Produto in {rel}")
sapato = quant.query(f"Produto in {sap}")
short = quant.query(f"Produto in {sho}")
sunga = quant.query(f"Produto in {sung}")
terno = quant.query(f"Produto in {ter}")
tenis = quant.query(f"Produto in {teni}")
dic2 = {}
axis1 = ['Bermudas','Calças','Camisas','Camisetas','Casacos','Chinelos','Cintos','Cuecas','Gorros','Meias','Mochilas','Polos','Pulseiras',
        'Relógios','Sapatos','Shorts','Sungas','Ternos','Tênis']
axis2 = []
axis2.append(bermuda['Quantidade'].sum())
axis2.append(calça['Quantidade'].sum())
axis2.append(camisa['Quantidade'].sum())
axis2.append(camiseta['Quantidade'].sum())
axis2.append(casaco['Quantidade'].sum())
axis2.append(chinelo['Quantidade'].sum())
axis2.append(cinto['Quantidade'].sum())
axis2.append(cueca['Quantidade'].sum())
axis2.append(gorro['Quantidade'].sum())
axis2.append(meia['Quantidade'].sum())
axis2.append(mochila['Quantidade'].sum())
axis2.append(polo['Quantidade'].sum())
axis2.append(pulseira['Quantidade'].sum())
axis2.append(relogio['Quantidade'].sum())
axis2.append(sapato['Quantidade'].sum())
axis2.append(short['Quantidade'].sum())
axis2.append(sunga['Quantidade'].sum())
axis2.append(terno['Quantidade'].sum())
axis2.append(tenis['Quantidade'].sum())
dic2['Produtos']=[]
dic2['Quantidade vendida']=[]
for pos,n in enumerate(axis1):
    dic2['Produtos'].append(n)
    dic2['Quantidade vendida'].append(axis2[pos])
dic2df = pd.DataFrame(dic2)
quanttot = dic2df['Quantidade vendida'].sum()
VCano = px.pie(dic2df, names='Produtos', values='Quantidade vendida', color='Produtos', template='plotly_dark', hole=0.3, title=f'Quantidade de produtos vendidos por categoria ({quanttot} produtos vendidos)',
           height=500)

# top 5 prod fat / % por canal

# SEMANAL
diacanal = make_subplots(rows=2, cols=3, specs=[[{'rowspan':2,'colspan':2,'type':'xy'}, None, {'rowspan':2,'type':'domain'}],
                                               [None, None, None]], subplot_titles=('5 produtos com maior faturamento','Vendas por canal',''))
diacanal.update_layout(template='plotly_dark')
diacanal.update_annotations(font_size=20)
nom=[]
fatr=[]
pfat = vendas[['Produto','Valor Final']].groupby('Produto').sum()
for c in range(0,5):
    nom.append(pfat.idxmax()['Valor Final'])
    fatr.append(pfat.max()['Valor Final'])
    for i in list(pfat.index):
        if pfat.loc[i,'Valor Final']==pfat.max()['Valor Final']:
            pfat = pfat.drop(i)
            break
dicp2 = {}
dicp2['Produto']=nom
dicp2['Faturamento']=fatr
datap2 = pd.DataFrame(dicp2)
diacanal.add_trace(go.Bar(x=list(datap2['Produto']), y=list(datap2['Faturamento']), marker=dict(color=('cyan','royalblue','blue','lightcyan','darkcyan'))), row=1, col=1)
diacanal.update_yaxes(title_text='Faturamento', row=1, col=1)

# adicionar canais de venda
canais = ['Loja fisica','Loja fisica','Loja fisica','Loja fisica','Instagram','Instagram','Instagram','Anúncios','Anúncios','Recomendação de amigos']
for i in list(vendas.index):
    vendas.loc[i,'Canal']=random.choice(canais)
c = ['Loja fisica','Instagram','Anúncios','Recomendação de amigos']
v = []
v.append(vendas['Canal'].value_counts()['Loja fisica'])
v.append(vendas['Canal'].value_counts()['Instagram'])
v.append(vendas['Canal'].value_counts()['Anúncios'])
v.append(vendas['Canal'].value_counts()['Recomendação de amigos'])
diacanal.add_trace(go.Pie(labels=c, values=v, marker=dict(colors=('cyan','royalblue','blue','lightcyan')), name='Produtos com + fat.'), row=1, col=3)

# QUINZENA
diacanal15 = make_subplots(rows=2, cols=3, specs=[[{'rowspan':2,'colspan':2,'type':'xy'}, None, {'rowspan':2,'type':'domain'}],
                                               [None, None, None]], subplot_titles=('5 produtos com maior faturamento','Vendas por canal',''))
diacanal15.update_layout(template='plotly_dark')
diacanal15.update_annotations(font_size=20)
nom=[]
fatr=[]
pfat = vds15[['Produto','Valor Final']].groupby('Produto').sum()
for c in range(0,5):
    nom.append(pfat.idxmax()['Valor Final'])
    fatr.append(pfat.max()['Valor Final'])
    for i in list(pfat.index):
        if pfat.loc[i,'Valor Final']==pfat.max()['Valor Final']:
            pfat = pfat.drop(i)
            break
dicp2 = {}
dicp2['Produto']=nom
dicp2['Faturamento']=fatr
datap2 = pd.DataFrame(dicp2)
diacanal15.add_trace(go.Bar(x=list(datap2['Produto']), y=list(datap2['Faturamento']), marker=dict(color=('cyan','royalblue','blue','lightcyan','darkcyan'))), row=1, col=1)
diacanal15.update_yaxes(title_text='Faturamento', row=1, col=1)

# adicionar canais de venda
canais = ['Loja fisica','Loja fisica','Loja fisica','Loja fisica','Instagram','Instagram','Instagram','Anúncios','Anúncios','Recomendação de amigos']
for i in list(vds15.index):
    vds15.loc[i,'Canal']=random.choice(canais)
c = ['Loja fisica','Instagram','Anúncios','Recomendação de amigos']
v = []
v.append(vds15['Canal'].value_counts()['Loja fisica'])
v.append(vds15['Canal'].value_counts()['Instagram'])
v.append(vds15['Canal'].value_counts()['Anúncios'])
v.append(vds15['Canal'].value_counts()['Recomendação de amigos'])
diacanal15.add_trace(go.Pie(labels=c, values=v, marker=dict(colors=('cyan','royalblue','blue','lightcyan')), name='Produtos com + fat.'), row=1, col=3)

# MENSAL
diacanal30 = make_subplots(rows=2, cols=3, specs=[[{'rowspan':2,'colspan':2,'type':'xy'}, None, {'rowspan':2,'type':'domain'}],
                                               [None, None, None]], subplot_titles=('5 produtos com maior faturamento','Vendas por canal',''))
diacanal30.update_layout(template='plotly_dark')
diacanal30.update_annotations(font_size=20)
nom=[]
fatr=[]
pfat = vds30[['Produto','Valor Final']].groupby('Produto').sum()
for c in range(0,5):
    nom.append(pfat.idxmax()['Valor Final'])
    fatr.append(pfat.max()['Valor Final'])
    for i in list(pfat.index):
        if pfat.loc[i,'Valor Final']==pfat.max()['Valor Final']:
            pfat = pfat.drop(i)
            break
dicp2 = {}
dicp2['Produto']=nom
dicp2['Faturamento']=fatr
datap2 = pd.DataFrame(dicp2)
diacanal30.add_trace(go.Bar(x=list(datap2['Produto']), y=list(datap2['Faturamento']), marker=dict(color=('cyan','royalblue','blue','lightcyan','darkcyan'))), row=1, col=1)
diacanal30.update_yaxes(title_text='Faturamento', row=1, col=1)

# adicionar canais de venda
canais = ['Loja fisica','Loja fisica','Loja fisica','Loja fisica','Instagram','Instagram','Instagram','Anúncios','Anúncios','Recomendação de amigos']
for i in list(vds30.index):
    vds30.loc[i,'Canal']=random.choice(canais)
c = ['Loja fisica','Instagram','Anúncios','Recomendação de amigos']
v = []
v.append(vds30['Canal'].value_counts()['Loja fisica'])
v.append(vds30['Canal'].value_counts()['Instagram'])
v.append(vds30['Canal'].value_counts()['Anúncios'])
v.append(vds30['Canal'].value_counts()['Recomendação de amigos'])
diacanal30.add_trace(go.Pie(labels=c, values=v, marker=dict(colors=('cyan','royalblue','blue','lightcyan')), name='Produtos com + fat.'), row=1, col=3)

# ANUAL
diacanalano = make_subplots(rows=2, cols=3, specs=[[{'rowspan':2,'colspan':2,'type':'xy'}, None, {'rowspan':2,'type':'domain'}],
                                               [None, None, None]], subplot_titles=('5 produtos com maior faturamento','Vendas por canal',''))
diacanalano.update_layout(template='plotly_dark')
diacanalano.update_annotations(font_size=20)
nom=[]
fatr=[]
pfat = vendasinit[['Produto','Valor Final']].groupby('Produto').sum()
for c in range(0,5):
    nom.append(pfat.idxmax()['Valor Final'])
    fatr.append(pfat.max()['Valor Final'])
    for i in list(pfat.index):
        if pfat.loc[i,'Valor Final']==pfat.max()['Valor Final']:
            pfat = pfat.drop(i)
            break
dicp2 = {}
dicp2['Produto']=nom
dicp2['Faturamento']=fatr
datap2 = pd.DataFrame(dicp2)
diacanalano.add_trace(go.Bar(x=list(datap2['Produto']), y=list(datap2['Faturamento']), marker=dict(color=('cyan','royalblue','blue','lightcyan','darkcyan'))), row=1, col=1)
diacanalano.update_yaxes(title_text='Faturamento', row=1, col=1)

# adicionar canais de venda
canais = ['Loja fisica','Loja fisica','Loja fisica','Loja fisica','Instagram','Instagram','Instagram','Anúncios','Anúncios','Recomendação de amigos']
for i in list(vendasinit.index):
    vendasinit.loc[i,'Canal']=random.choice(canais)
c = ['Loja fisica','Instagram','Anúncios','Recomendação de amigos']
v = []
v.append(vendasinit['Canal'].value_counts()['Loja fisica'])
v.append(vendasinit['Canal'].value_counts()['Instagram'])
v.append(vendasinit['Canal'].value_counts()['Anúncios'])
v.append(vendasinit['Canal'].value_counts()['Recomendação de amigos'])
diacanalano.add_trace(go.Pie(labels=c, values=v, marker=dict(colors=('cyan','royalblue','blue','lightcyan')), name='Produtos com + fat.'), row=1, col=3)

# produtos mais vendidos pro cliente ideal

# SEMANAL
perfgeral = make_subplots(rows=8, cols=4, specs=[[{'rowspan':3,'colspan':2,'type':'xy'}, None, {'rowspan':3,'colspan':2,'type':'xy'}, None],
                                                [None, None, None, None],
                                                [None, None, None, None],
                                                [None, None, None, None],
                                                [None, None, None, None],
                                                [None, None, None, None],
                                                [None, {'rowspan':2,'colspan':2,'type':'xy'}, None, None],
                                                [None, None, None, None],], subplot_titles=['Produtos mais vendidos p/ cliente ideal','Produtos mais vendidos no geral','Produtos menos vendidos no geral'])
perfgeral.update_layout(template='plotly_dark')
perfgeral.update_annotations(font_size=20)
perfil = vendas.query('Idade>=18 and Idade<=50 and Sexo=="Homem"')
prodperf = perfil[['Produto','Quantidade']].groupby('Produto').sum()
eixox = []
eixoy = []
for c in range(0,10):
    eixox.append(prodperf.idxmax()['Quantidade'])
    eixoy.append(prodperf.max()['Quantidade'])
    prodperf = prodperf.drop(prodperf.idxmax()['Quantidade'], axis=0)
# top10 geral mais/menos vendidos
prodgeral = vendas[['Produto','Quantidade']].groupby('Produto').sum()
eixox1 = []
eixoy1 = []
for c in range(0,10):
    eixox1.append(prodgeral.idxmax()['Quantidade'])
    eixoy1.append(prodgeral.max()['Quantidade'])
    prodgeral = prodgeral.drop(prodgeral.idxmax()['Quantidade'], axis=0)
perfgeral.add_trace(go.Bar(x=eixox, y=eixoy, marker=dict(color=['cyan','cyan','cyan','cyan','cyan','cyan','cyan','cyan','cyan','cyan']), name='Cliente Ideal'), row=1, col=1)
perfgeral.add_trace(go.Bar(x=eixox1, y=eixoy1, marker=dict(color=['yellow','yellow','yellow','yellow','yellow','yellow','yellow','yellow','yellow','yellow']), name='Mais vendidos no geral'), row=1, col=3)
perfgeral.update_yaxes(title_text='Quantidade vendida', row=1, col=1)
eixox2 = []
eixoy2 = []
for c in range(0,10):
    eixox2.append(prodperf.idxmin()['Quantidade'])
    eixoy2.append(prodperf.min()['Quantidade'])
    prodperf = prodperf.drop(prodperf.idxmin()['Quantidade'], axis=0)
perfgeral.add_trace(go.Bar(x=eixox2, y=eixoy2, marker=dict(color=['red','red','red','red','red','red','red','red','red','red']), name='Menos vendidos no geral'), row=7, col=2)
perfgeral.update_yaxes(title_text='Quantidade vendida', row=7, col=2)


# QUINZENA
perfgeral15 = make_subplots(rows=8, cols=4, specs=[[{'rowspan':3,'colspan':2,'type':'xy'}, None, {'rowspan':3,'colspan':2,'type':'xy'}, None],
                                                [None, None, None, None],
                                                [None, None, None, None],
                                                [None, None, None, None],
                                                [None, None, None, None],
                                                [None, None, None, None],
                                                [None, {'rowspan':2,'colspan':2,'type':'xy'}, None, None],
                                                [None, None, None, None],], subplot_titles=['Produtos mais vendidos p/ cliente ideal','Produtos mais vendidos no geral','Produtos menos vendidos no geral'])
perfgeral15.update_layout(template='plotly_dark')
perfgeral15.update_annotations(font_size=20)
perfil = vds15.query('Idade>=18 and Idade<=50 and Sexo=="Homem"')
prodperf = perfil[['Produto','Quantidade']].groupby('Produto').sum()
eixox = []
eixoy = []
for c in range(0,10):
    eixox.append(prodperf.idxmax()['Quantidade'])
    eixoy.append(prodperf.max()['Quantidade'])
    prodperf = prodperf.drop(prodperf.idxmax()['Quantidade'], axis=0)
# top10 geral mais/menos vendidos
prodgeral = vds15[['Produto','Quantidade']].groupby('Produto').sum()
eixox1 = []
eixoy1 = []
for c in range(0,10):
    eixox1.append(prodgeral.idxmax()['Quantidade'])
    eixoy1.append(prodgeral.max()['Quantidade'])
    prodgeral = prodgeral.drop(prodgeral.idxmax()['Quantidade'], axis=0)
perfgeral15.add_trace(go.Bar(x=eixox, y=eixoy, marker=dict(color=['cyan','cyan','cyan','cyan','cyan','cyan','cyan','cyan','cyan','cyan']), name='Cliente Ideal'), row=1, col=1)
perfgeral15.add_trace(go.Bar(x=eixox1, y=eixoy1, marker=dict(color=['yellow','yellow','yellow','yellow','yellow','yellow','yellow','yellow','yellow','yellow']), name='Mais vendidos no geral'), row=1, col=3)
perfgeral15.update_yaxes(title_text='Quantidade vendida', row=1, col=1)
eixox2 = []
eixoy2 = []
for c in range(0,10):
    eixox2.append(prodperf.idxmin()['Quantidade'])
    eixoy2.append(prodperf.min()['Quantidade'])
    prodperf = prodperf.drop(prodperf.idxmin()['Quantidade'], axis=0)
perfgeral15.add_trace(go.Bar(x=eixox2, y=eixoy2, marker=dict(color=['red','red','red','red','red','red','red','red','red','red']), name='Menos vendidos no geral'), row=7, col=2)
perfgeral15.update_yaxes(title_text='Quantidade vendida', row=7, col=2)

# MENSAL
perfgeral30 = make_subplots(rows=8, cols=4, specs=[[{'rowspan':3,'colspan':2,'type':'xy'}, None, {'rowspan':3,'colspan':2,'type':'xy'}, None],
                                                [None, None, None, None],
                                                [None, None, None, None],
                                                [None, None, None, None],
                                                [None, None, None, None],
                                                [None, None, None, None],
                                                [None, {'rowspan':2,'colspan':2,'type':'xy'}, None, None],
                                                [None, None, None, None],], subplot_titles=['Produtos mais vendidos p/ cliente ideal','Produtos mais vendidos no geral','Produtos menos vendidos no geral'])
perfgeral30.update_layout(template='plotly_dark')
perfgeral30.update_annotations(font_size=20)
perfil = vds30.query('Idade>=18 and Idade<=50 and Sexo=="Homem"')
prodperf = perfil[['Produto','Quantidade']].groupby('Produto').sum()
eixox = []
eixoy = []
for c in range(0,10):
    eixox.append(prodperf.idxmax()['Quantidade'])
    eixoy.append(prodperf.max()['Quantidade'])
    prodperf = prodperf.drop(prodperf.idxmax()['Quantidade'], axis=0)
# top10 geral mais/menos vendidos
prodgeral = vds30[['Produto','Quantidade']].groupby('Produto').sum()
eixox1 = []
eixoy1 = []
for c in range(0,10):
    eixox1.append(prodgeral.idxmax()['Quantidade'])
    eixoy1.append(prodgeral.max()['Quantidade'])
    prodgeral = prodgeral.drop(prodgeral.idxmax()['Quantidade'], axis=0)
perfgeral30.add_trace(go.Bar(x=eixox, y=eixoy, marker=dict(color=['cyan','cyan','cyan','cyan','cyan','cyan','cyan','cyan','cyan','cyan']), name='Cliente Ideal'), row=1, col=1)
perfgeral30.add_trace(go.Bar(x=eixox1, y=eixoy1, marker=dict(color=['yellow','yellow','yellow','yellow','yellow','yellow','yellow','yellow','yellow','yellow']), name='Mais vendidos no geral'), row=1, col=3)
perfgeral30.update_yaxes(title_text='Quantidade vendida', row=1, col=1)
eixox2 = []
eixoy2 = []
for c in range(0,10):
    eixox2.append(prodperf.idxmin()['Quantidade'])
    eixoy2.append(prodperf.min()['Quantidade'])
    prodperf = prodperf.drop(prodperf.idxmin()['Quantidade'], axis=0)
perfgeral30.add_trace(go.Bar(x=eixox2, y=eixoy2, marker=dict(color=['red','red','red','red','red','red','red','red','red','red']), name='Menos vendidos no geral'), row=7, col=2)
perfgeral30.update_yaxes(title_text='Quantidade vendida', row=7, col=2)


# ANUAL
perfgeralano = make_subplots(rows=8, cols=4, specs=[[{'rowspan':3,'colspan':2,'type':'xy'}, None, {'rowspan':3,'colspan':2,'type':'xy'}, None],
                                                [None, None, None, None],
                                                [None, None, None, None],
                                                [None, None, None, None],
                                                [None, None, None, None],
                                                [None, None, None, None],
                                                [None, {'rowspan':2,'colspan':2,'type':'xy'}, None, None],
                                                [None, None, None, None],], subplot_titles=['Produtos mais vendidos p/ cliente ideal','Produtos mais vendidos no geral','Produtos menos vendidos no geral'])
perfgeralano.update_layout(template='plotly_dark')
perfgeralano.update_annotations(font_size=20)
perfil = vendasinit.query('Idade>=18 and Idade<=50 and Sexo=="Homem"')
prodperf = perfil[['Produto','Quantidade']].groupby('Produto').sum()
eixox = []
eixoy = []
for c in range(0,10):
    eixox.append(prodperf.idxmax()['Quantidade'])
    eixoy.append(prodperf.max()['Quantidade'])
    prodperf = prodperf.drop(prodperf.idxmax()['Quantidade'], axis=0)
# top10 geral mais/menos vendidos
prodgeral = vendasinit[['Produto','Quantidade']].groupby('Produto').sum()
eixox1 = []
eixoy1 = []
for c in range(0,10):
    eixox1.append(prodgeral.idxmax()['Quantidade'])
    eixoy1.append(prodgeral.max()['Quantidade'])
    prodgeral = prodgeral.drop(prodgeral.idxmax()['Quantidade'], axis=0)
perfgeralano.add_trace(go.Bar(x=eixox, y=eixoy, marker=dict(color=['cyan','cyan','cyan','cyan','cyan','cyan','cyan','cyan','cyan','cyan']), name='Cliente Ideal'), row=1, col=1)
perfgeralano.add_trace(go.Bar(x=eixox1, y=eixoy1, marker=dict(color=['yellow','yellow','yellow','yellow','yellow','yellow','yellow','yellow','yellow','yellow']), name='Mais vendidos no geral'), row=1, col=3)
perfgeralano.update_yaxes(title_text='Quantidade vendida', row=1, col=1)
eixox2 = []
eixoy2 = []
for c in range(0,10):
    eixox2.append(prodperf.idxmin()['Quantidade'])
    eixoy2.append(prodperf.min()['Quantidade'])
    prodperf = prodperf.drop(prodperf.idxmin()['Quantidade'], axis=0)
perfgeralano.add_trace(go.Bar(x=eixox2, y=eixoy2, marker=dict(color=['red','red','red','red','red','red','red','red','red','red']), name='Menos vendidos no geral'), row=7, col=2)
perfgeralano.update_yaxes(title_text='Quantidade vendida', row=7, col=2)

# Controle de estoque

# SEMANAL
prods = vendas[['Produto','Quantidade']].groupby('Produto').sum()
est = vendasinit[['Produto','Quantidade']].groupby('Produto').sum()
for c in list(est.index):
    est.loc[c,'Produto']=c
for c in list(est.index):
    est.loc[c,'Estoque inicial']=est.loc[c,'Quantidade']*(1 + random.randint(50,70)/100)
for p in list(est.index):
    est.loc[p,'Estoque inicial']=math.floor(est.loc[p,'Estoque inicial'])
for p in list(est.index):
    est.loc[p,'Produto']=p
est = est.drop('Quantidade', axis=1)
for p in list(est.index):
    if p not in (prods.index):
        est.loc[p,'Quantidade vendida']=0
    else:
        est.loc[p,'Quantidade vendida']=prods.loc[p,'Quantidade']
for p in list(est.index):
    est.loc[p,'Estoque atual']=est.loc[p,'Estoque inicial']-est.loc[p,'Quantidade vendida']

listp1 = []
listp2 = []
listp3 = []
listp4 = []
for pos,p in enumerate(list(est.index)):
    if pos<=30:
        listp1.append(p)
    if 30<pos<=60:
        listp2.append(p)
    if 60<pos<=90:
        listp3.append(p)
    if 90<pos:
        listp4.append(p)
est1 = est.loc[listp1,['Estoque inicial','Quantidade vendida','Estoque atual','Produto']]
est2 = est.loc[listp2,['Estoque inicial','Quantidade vendida','Estoque atual','Produto']]
est3 = est.loc[listp3,['Estoque inicial','Quantidade vendida','Estoque atual','Produto']]
est4 = est.loc[listp4,['Estoque inicial','Quantidade vendida','Estoque atual','Produto']]

grafest1 = px.bar(est1, x='Produto', y=['Estoque inicial','Quantidade vendida','Estoque atual'], barmode='group',color_discrete_map={'Estoque inicial':'yellow','Quantidade vendida':'cyan','Estoque atual':'purple'},
                  template='plotly_dark', title='Controle de estoque', height=400)
grafest2 = px.bar(est2, x='Produto', y=['Estoque inicial','Quantidade vendida','Estoque atual'], barmode='group',color_discrete_map={'Estoque inicial':'yellow','Quantidade vendida':'cyan','Estoque atual':'purple'},
                  template='plotly_dark', height=400)
grafest3 = px.bar(est3, x='Produto', y=['Estoque inicial','Quantidade vendida','Estoque atual'], barmode='group',color_discrete_map={'Estoque inicial':'yellow','Quantidade vendida':'cyan','Estoque atual':'purple'},
                  template='plotly_dark', height=400)
grafest4 = px.bar(est4, x='Produto', y=['Estoque inicial','Quantidade vendida','Estoque atual'], barmode='group',color_discrete_map={'Estoque inicial':'yellow','Quantidade vendida':'cyan','Estoque atual':'purple'},
                  template='plotly_dark', height=400)

# QUINZENA
prods = vds15[['Produto','Quantidade']].groupby('Produto').sum()
for p in list(est.index):
    if p not in (prods.index):
        est.loc[p,'Quantidade vendida semanal']=0
    else:
        est.loc[p,'Quantidade vendida semanal']=prods.loc[p,'Quantidade']
for p in list(est.index):
    est.loc[p,'Estoque atual semanal']=est.loc[p,'Estoque inicial']-est.loc[p,'Quantidade vendida semanal']

listp1 = []
listp2 = []
listp3 = []
listp4 = []
for pos,p in enumerate(list(est.index)):
    if pos<=30:
        listp1.append(p)
    if 30<pos<=60:
        listp2.append(p)
    if 60<pos<=90:
        listp3.append(p)
    if 90<pos:
        listp4.append(p)
est1 = est.loc[listp1,['Estoque inicial','Quantidade vendida semanal','Estoque atual semanal','Produto']]
est2 = est.loc[listp2,['Estoque inicial','Quantidade vendida semanal','Estoque atual semanal','Produto']]
est3 = est.loc[listp3,['Estoque inicial','Quantidade vendida semanal','Estoque atual semanal','Produto']]
est4 = est.loc[listp4,['Estoque inicial','Quantidade vendida semanal','Estoque atual semanal','Produto']]

grafest115 = px.bar(est1, x='Produto', y=['Estoque inicial','Quantidade vendida semanal','Estoque atual semanal'], barmode='group',color_discrete_map={'Estoque inicial':'yellow','Quantidade vendida':'cyan','Estoque atual':'purple'},
                  template='plotly_dark', title='Controle de estoque', height=400)
grafest215 = px.bar(est2, x='Produto', y=['Estoque inicial','Quantidade vendida semanal','Estoque atual semanal'], barmode='group',color_discrete_map={'Estoque inicial':'yellow','Quantidade vendida':'cyan','Estoque atual':'purple'},
                  template='plotly_dark', height=400)
grafest315 = px.bar(est3, x='Produto', y=['Estoque inicial','Quantidade vendida semanal','Estoque atual semanal'], barmode='group',color_discrete_map={'Estoque inicial':'yellow','Quantidade vendida':'cyan','Estoque atual':'purple'},
                  template='plotly_dark', height=400)
grafest415 = px.bar(est4, x='Produto', y=['Estoque inicial','Quantidade vendida semanal','Estoque atual semanal'], barmode='group',color_discrete_map={'Estoque inicial':'yellow','Quantidade vendida':'cyan','Estoque atual':'purple'},
                  template='plotly_dark', height=400)

# MENSAL
prods = vds30[['Produto','Quantidade']].groupby('Produto').sum()
for p in list(est.index):
    if p not in (prods.index):
        est.loc[p,'Quantidade vendida mensal']=0
    else:
        est.loc[p,'Quantidade vendida mensal']=prods.loc[p,'Quantidade']
for p in list(est.index):
    est.loc[p,'Estoque atual mensal']=est.loc[p,'Estoque inicial']-est.loc[p,'Quantidade vendida mensal']

listp1 = []
listp2 = []
listp3 = []
listp4 = []
for pos,p in enumerate(list(est.index)):
    if pos<=30:
        listp1.append(p)
    if 30<pos<=60:
        listp2.append(p)
    if 60<pos<=90:
        listp3.append(p)
    if 90<pos:
        listp4.append(p)
est1 = est.loc[listp1,['Estoque inicial','Quantidade vendida mensal','Estoque atual mensal','Produto']]
est2 = est.loc[listp2,['Estoque inicial','Quantidade vendida mensal','Estoque atual mensal','Produto']]
est3 = est.loc[listp3,['Estoque inicial','Quantidade vendida mensal','Estoque atual mensal','Produto']]
est4 = est.loc[listp4,['Estoque inicial','Quantidade vendida mensal','Estoque atual mensal','Produto']]

grafest130 = px.bar(est1, x='Produto', y=['Estoque inicial','Quantidade vendida mensal','Estoque atual mensal'], barmode='group',color_discrete_map={'Estoque inicial':'yellow','Quantidade vendida':'cyan','Estoque atual':'purple'},
                  template='plotly_dark', title='Controle de estoque', height=400)
grafest230 = px.bar(est2, x='Produto', y=['Estoque inicial','Quantidade vendida mensal','Estoque atual mensal'], barmode='group',color_discrete_map={'Estoque inicial':'yellow','Quantidade vendida':'cyan','Estoque atual':'purple'},
                  template='plotly_dark', height=400)
grafest330 = px.bar(est3, x='Produto', y=['Estoque inicial','Quantidade vendida mensal','Estoque atual mensal'], barmode='group',color_discrete_map={'Estoque inicial':'yellow','Quantidade vendida':'cyan','Estoque atual':'purple'},
                  template='plotly_dark', height=400)
grafest430 = px.bar(est4, x='Produto', y=['Estoque inicial','Quantidade vendida mensal','Estoque atual mensal'], barmode='group',color_discrete_map={'Estoque inicial':'yellow','Quantidade vendida':'cyan','Estoque atual':'purple'},
                  template='plotly_dark', height=400)


# ANUAL
prods = vendasinit[['Produto','Quantidade']].groupby('Produto').sum()
for p in list(est.index):
    if p not in (prods.index):
        est.loc[p,'Quantidade vendida anual']=0
    else:
        est.loc[p,'Quantidade vendida anual']=prods.loc[p,'Quantidade']
for p in list(est.index):
    est.loc[p,'Estoque atual anual']=est.loc[p,'Estoque inicial']-est.loc[p,'Quantidade vendida anual']

listp1 = []
listp2 = []
listp3 = []
listp4 = []
for pos,p in enumerate(list(est.index)):
    if pos<=30:
        listp1.append(p)
    if 30<pos<=60:
        listp2.append(p)
    if 60<pos<=90:
        listp3.append(p)
    if 90<pos:
        listp4.append(p)
est1 = est.loc[listp1,['Estoque inicial','Quantidade vendida anual','Estoque atual anual','Produto']]
est2 = est.loc[listp2,['Estoque inicial','Quantidade vendida anual','Estoque atual anual','Produto']]
est3 = est.loc[listp3,['Estoque inicial','Quantidade vendida anual','Estoque atual anual','Produto']]
est4 = est.loc[listp4,['Estoque inicial','Quantidade vendida anual','Estoque atual anual','Produto']]

grafest1ano = px.bar(est1, x='Produto', y=['Estoque inicial','Quantidade vendida anual','Estoque atual anual'], barmode='group',color_discrete_map={'Estoque inicial':'yellow','Quantidade vendida':'cyan','Estoque atual':'purple'},
                  template='plotly_dark', title='Controle de estoque', height=400)
grafest2ano = px.bar(est2, x='Produto', y=['Estoque inicial','Quantidade vendida anual','Estoque atual anual'], barmode='group',color_discrete_map={'Estoque inicial':'yellow','Quantidade vendida':'cyan','Estoque atual':'purple'},
                  template='plotly_dark', height=400)
grafest3ano = px.bar(est3, x='Produto', y=['Estoque inicial','Quantidade vendida anual','Estoque atual anual'], barmode='group',color_discrete_map={'Estoque inicial':'yellow','Quantidade vendida':'cyan','Estoque atual':'purple'},
                  template='plotly_dark', height=400)
grafest4ano = px.bar(est4, x='Produto', y=['Estoque inicial','Quantidade vendida anual','Estoque atual anual'], barmode='group',color_discrete_map={'Estoque inicial':'yellow','Quantidade vendida':'cyan','Estoque atual':'purple'},
                  template='plotly_dark', height=400)
# VOLUME DE VENDAS

# SEMANAL
d = []
v = []
for c in range(1,8):
    v.append(vendas['Dia'].value_counts()[c])
    d.append(c)
vol = px.line(x=d, y=v, template='plotly_dark', title='Volume de vendas ao longo da semana', labels={'x':'Dia','y':'Quantidade de vendas'},
             color_discrete_sequence=['green'], markers=True)

# QUINZENA
d = []
v = []
for c in range(1,16):
    v.append(vds15['Dia'].value_counts()[c])
    d.append(c)
vol15 = px.line(x=d, y=v, template='plotly_dark', title='Volume de vendas ao longo da quinzena', labels={'x':'Dia','y':'Quantidade de vendas'},
             color_discrete_sequence=['green'], markers=True)

# MENSAL
d = []
v = []
for c in range(1,29):
    v.append(vds30['Dia'].value_counts()[c])
    d.append(c)
vol30 = px.line(x=d, y=v, template='plotly_dark', title='Volume de vendas ao longo do mês', labels={'x':'Dia','y':'Quantidade de vendas'},
             color_discrete_sequence=['green'], markers=True)

# ANUAL 
d = []
v = []
for c in list(fatano.index):
    v.append(vendasinit['Mês'].value_counts()[c])
    d.append(c)
volano = px.line(x=d, y=v, template='plotly_dark', title='Volume de vendas ao longo do ano', labels={'x':'Mês','y':'Quantidade de vendas'},
             color_discrete_sequence=['green'], markers=True)

# comparação de fat, tic, vendas, produtos vendidos
vendasf = vendasinit.query('Mês == 2')
vendasm = vendasinit.query('Mês == 3')

fatfev = vendasf[['Dia','Valor Final','Lucro']].groupby('Dia').sum()
fatmar = vendasm[['Dia','Valor Final','Lucro']].groupby('Dia').sum()

for d in list(fatfev.index):
    fatfev.loc[d,'Dia']=d
fatfev['Mês']='Fevereiro'
for d in list(fatmar.index):
    fatmar.loc[d,'Dia']=d
fatmar['Mês']='Março'

qfev = vendasf['Dia'].value_counts()
qmar = vendasm['Dia'].value_counts()
for i in list(fatfev.index):
    fatfev.loc[i,'Quantidade de vendas']=qfev[i]
fatfev['Ticket']=fatfev['Valor Final']/fatfev['Quantidade de vendas']
ticfev=fatfev['Ticket'].mean()
fatfevereiro = fatfev['Valor Final'].sum()
quantfev = fatfev['Quantidade de vendas'].sum()
prodsfev = vendasf['Quantidade'].sum()

for i in list(fatmar.index):
    fatmar.loc[i,'Quantidade de vendas']=qmar[i]
fatmar['Ticket']=fatmar['Valor Final']/fatmar['Quantidade de vendas']
ticmar=fatmar['Ticket'].mean()
fatmarço = fatmar['Valor Final'].sum()
quantmar = fatmar['Quantidade de vendas'].sum()
prodsmar = vendasm['Quantidade'].sum()

diffat = fatmarço - fatfevereiro
diftic = ticmar - ticfev
difquant = quantmar - quantfev
difprod =  prodsmar - prodsfev

compfat = pd.concat([fatfev,fatmar], axis=0)
compfat.rename(columns={'Valor Final':'Faturamento diário','Lucro':'Lucro diário'}, inplace=True)

# fat e vendas diarias
graffat = px.line(compfat, x='Dia', y='Faturamento diário', color='Mês', template='plotly_dark', color_discrete_sequence=['red','white'],
                  title=f'Comparação do faturamento diário')
grafvend = px.bar(compfat, x='Dia', y='Quantidade de vendas', color='Mês', barmode='group', template='plotly_dark', color_discrete_map={'Fevereiro':'cyan','Março':'lightcyan'},
                  title=f'Comparação do volume de vendas')

# tic., fat., vendas, prod. vendidos
fevxmar = make_subplots(rows=4, cols=4, specs=[[{'rowspan':4,'type':'xy'}, {'rowspan':4,'type':'xy'}, {'rowspan':4,'type':'xy'}, {'rowspan':4,'type':'xy'}],
                                              [None, None, None, None],
                                              [None, None, None, None],
                                              [None, None, None, None]], subplot_titles=['Fator: Faturamento','Fator: Ticket médio','Fator: Vendas','Fator: Produtos vendidos'])
fevxmar.update_layout(template='plotly_dark')
fevxmar.update_annotations(font_size=20)
fevxmar.add_trace(go.Bar(x=['Fevereiro','Março'], y=[fatfevereiro, fatmarço], marker=dict(color=['red','white']), name='Faturamento'), row=1, col=1)
fevxmar.add_annotation(x='Março', y=fatmarço, text=f'+R${diffat}', row=1, col=1)

fevxmar.add_trace(go.Bar(x=['Fevereiro','Março'], y=[ticfev, ticmar], marker=dict(color=['red','white']), name='Ticket médio'), row=1, col=2)
fevxmar.add_annotation(x='Março', y=ticmar, text=f'+R${diftic:.1f}', row=1, col=2)
                        
fevxmar.add_trace(go.Bar(x=['Fevereiro','Março'], y=[quantfev, quantmar], marker=dict(color=['red','white']), name='Vendas'), row=1, col=3)
fevxmar.add_annotation(x='Março', y=quantmar, text=f'+{difquant}', row=1, col=3)

fevxmar.add_trace(go.Bar(x=['Fevereiro','Março'], y=[prodsfev, prodsmar], marker=dict(color=['red','white']), name='Produtos vendidos'), row=1, col=4)
fevxmar.add_annotation(x='Março', y=prodsmar, text=f'+{difprod}', row=1, col=4)

# canais de venda
canais= ['Loja fisica','Instagram','Anúncios','Recomendação de amigos']
canaisfev = vendasf['Canal'].value_counts()
canaismar = vendasm['Canal'].value_counts()
axis3 = []
axis4 = []
for canal in canais:
    axis3.append(canaisfev[canal])
    axis4.append(canaismar[canal])
difloja = axis4[0] - axis3[0]
difinsta = axis4[1] - axis3[1]
difanun = axis4[2] - axis3[2]
difrec = axis4[3] - axis3[3]

fevxmar1 = make_subplots(rows=4, cols=4, specs=[[{'rowspan':4,'type':'xy'}, {'rowspan':4,'type':'xy'}, {'rowspan':4,'type':'xy'}, {'rowspan':4,'type':'xy'}],
                                              [None, None, None, None],
                                              [None, None, None, None],
                                              [None, None, None, None]], subplot_titles=['Fator: Loja fisica','Fator: Instagram','Fator: Anúncios','Fator: Recomendação'])
fevxmar1.update_layout(template='plotly_dark')
fevxmar1.update_annotations(font_size=20)
fevxmar1.add_trace(go.Bar(x=['Fevereiro','Março'], y=[axis3[0], axis4[0]], marker=dict(color=['cyan','lightcyan']), name='Loja fisica'), row=1, col=1)
fevxmar1.add_annotation(x='Março', y=axis4[0], text=f'+{difloja}', row=1, col=1)

fevxmar1.add_trace(go.Bar(x=['Fevereiro','Março'], y=[axis3[1], axis4[1]], marker=dict(color=['cyan','lightcyan']), name='Instagram'), row=1, col=2)
fevxmar1.add_annotation(x='Março', y=axis4[1], text=f'+{difinsta}', row=1, col=2)

fevxmar1.add_trace(go.Bar(x=['Fevereiro','Março'], y=[axis3[2], axis4[2]], marker=dict(color=['cyan','lightcyan']), name='Anúncios'), row=1, col=3)
fevxmar1.add_annotation(x='Março', y=axis4[2], text=f'+{difanun}', row=1, col=3)

fevxmar1.add_trace(go.Bar(x=['Fevereiro','Março'], y=[axis3[3], axis4[3]], marker=dict(color=['cyan','lightcyan']), name='Recomendação'), row=1, col=4)
fevxmar1.add_annotation(x='Março', y=axis3[3], text=f'{difrec}', row=1, col=4)


# previsão de estoque
prodxquant = vendasinit[['Produto','Quantidade']].groupby('Produto').sum()
corprev = []
cormed = []
for i in list(prodxquant.index):
    prodxquant.loc[i,'Venda média por mês']=math.ceil(prodxquant.loc[i,'Quantidade']/12)
    prodxquant.loc[i,'Estoque previsto']=prodxquant.loc[i,'Venda média por mês']*12
    
dic1 = {}
dic1['Produto']=[]
dic1['Quantidade']=[]
dic1['Venda média por mês']=[]
dic1['Estoque previsto']=[]
for i in list(prodxquant.index)[0:40]:
    dic1['Venda média por mês'].append(prodxquant.loc[i,'Venda média por mês'])
    dic1['Produto'].append(i)
    dic1['Quantidade'].append(prodxquant.loc[i,'Quantidade'])
    dic1['Estoque previsto'].append(prodxquant.loc[i,'Estoque previsto'])
    corprev.append('purple')
    cormed.append('lightcyan')
df1 = pd.DataFrame(dic1)
dic2 = {}
dic2['Produto']=[]
dic2['Quantidade']=[]
dic2['Venda média por mês']=[]
dic2['Estoque previsto']=[]
for i in list(prodxquant.index)[40:80]:
    dic2['Venda média por mês'].append(prodxquant.loc[i,'Venda média por mês'])
    dic2['Produto'].append(i)
    dic2['Quantidade'].append(prodxquant.loc[i,'Quantidade'])
    dic2['Estoque previsto'].append(prodxquant.loc[i,'Estoque previsto'])
df2 = pd.DataFrame(dic2)
dic3 = {}
dic3['Produto']=[]
dic3['Quantidade']=[]
dic3['Venda média por mês']=[]
dic3['Estoque previsto']=[]
for i in list(prodxquant.index)[80:121]:
    dic3['Venda média por mês'].append(prodxquant.loc[i,'Venda média por mês'])
    dic3['Produto'].append(i)
    dic3['Quantidade'].append(prodxquant.loc[i,'Quantidade'])
    dic3['Estoque previsto'].append(prodxquant.loc[i,'Estoque previsto'])
df3 = pd.DataFrame(dic3)

estprev1 = px.bar(df1, x='Produto', y='Estoque previsto', template='plotly_dark', color_discrete_sequence=corprev, height=500, title='Estoque para 1 ano (baseado na quantidade média vendida de cada produto)')
estmed1 = px.bar(df1, x='Produto', y='Venda média por mês', template='plotly_dark', color_discrete_sequence=cormed, height=400, title='Quantidade vendida em média de cada produto por mês')

estprev2 = px.bar(df2, x='Produto', y='Estoque previsto', template='plotly_dark', color_discrete_sequence=corprev, height=500)
estmed2 = px.bar(df2, x='Produto', y='Venda média por mês', template='plotly_dark', color_discrete_sequence=cormed, height=400)

estprev3 = px.bar(df3, x='Produto', y='Estoque previsto', template='plotly_dark', color_discrete_sequence=corprev, height=500)
estmed3 = px.bar(df3, x='Produto', y='Venda média por mês', template='plotly_dark', color_discrete_sequence=cormed, height=400)

# APP
app =  Dash(__name__)
server = app.server

# INSIDE
app.layout = html.Div(children=[
    html.H1(children='ANÁLISE DE VENDAS (FEVEREIRO)', id = 'Titulo'),
    dcc.Dropdown(['Semanal','Quinzena','Mensal','Anual'], value='Semanal', id = 'botao'),
    dcc.Graph(id = 'G', figure = fl7),
    dcc.Graph(id = 'H', figure = vol),
    dcc.Graph(id = 'G0', figure = ticxd),
    dcc.Graph(id = 'G1', figure = comp3),
    dcc.Graph(id = 'G2', figure = comp6),
    dcc.Graph(id = 'G3', figure = comp9),
    dcc.Graph(id = 'G4', figure = comp12),
    dcc.Graph(id = 'G5', figure = comp15),
    dcc.Graph(id = 'G6', figure = comp18),
    dcc.Graph(id = 'G7', figure = comp21),
    dcc.Graph(id = 'G8', figure = vxi),
    dcc.Graph(id = 'G9', figure = VC),
    dcc.Graph(id = 'G10', figure = diacanal),
    dcc.Graph(id = 'G11', figure = perfgeral),
    dcc.Graph(id = 'G12', figure = grafest1),
    dcc.Graph(id = 'G13', figure = grafest2),
    dcc.Graph(id = 'G14', figure = grafest3),
    dcc.Graph(id = 'G15', figure = grafest4),
    dcc.Dropdown(['Média vendida por produto','Previsão de estoque'], value='Previsão de estoque', id = 'botao1'),
    dcc.Graph(id = 'H1', figure = estprev1),
    dcc.Graph(id = 'H2', figure = estprev2),
    dcc.Graph(id = 'H3', figure = estprev3),
    html.H1(children='COMPARAÇÃO DE VENDAS (FEVEREIRO x MARÇO)'),
    dcc.Graph(id = 'G16', figure = graffat),
    dcc.Graph(id = 'G17', figure = grafvend),
    dcc.Graph(id = 'G18', figure = fevxmar),
    dcc.Graph(id = 'G19', figure = fevxmar1)
])

# callbacks

@app.callback(Output('Titulo','children'),
             Input('botao','value'))
def update_titulo(value):
    if value=='Semanal':
        return 'ANÁLISE DE VENDAS SEMANAL'
    if value=='Quinzena':
        return 'ANÁLISE DE VENDAS QUINZENA'
    if value=='Mensal':
        return 'ANÁLISE DE VENDAS MENSAL (Fevereiro)'
    if value=='Anual':
        return 'ANÁLISE DE VENDAS ANUAL'

@app.callback(Output('H1','figure'),
             Input('botao1','value'))
def update_estprev1(value):
    if value=='Previsão de estoque':
        return estprev1
    if value=='Média vendida por produto':
        return estmed1

@app.callback(Output('H2','figure'),
             Input('botao1','value'))
def update_estprev2(value):
    if value=='Previsão de estoque':
        return estprev2
    if value=='Média vendida por produto':
        return estmed2

@app.callback(Output('H3','figure'),
             Input('botao1','value'))
def update_estprev3(value):
    if value=='Previsão de estoque':
        return estprev3
    if value=='Média vendida por produto':
        return estmed3

@app.callback(Output('G','figure'),
             Input('botao','value'))
def update_fatxluc(value):
    if value=='Semanal':
        return fl7
    if value=='Quinzena':
        return fl15
    if value=='Mensal':
        return fl30
    if value=='Anual':
        return flano

@app.callback(Output('H','figure'),
             Input('botao','value'))
def update_vol(value):
    if value=='Semanal':
        return vol
    if value=='Quinzena':
        return vol15
    if value=='Mensal':
        return vol30
    if value=='Anual':
        return volano
        
@app.callback(Output('G0','figure'),
             Input('botao','value'))
def update_ticxd(value):
    if value=='Semanal':
        return ticxd
    if value=='Quinzena':
        return ticxd15
    if value=='Mensal':
        return ticxd30
    if value=='Anual':
        return ticxdano

@app.callback(Output('G1','figure'),
             Input('botao','value'))
def update_comp3(value):
    if value=='Semanal':
        return comp3
    if value=='Quinzena':
        return comp315
    if value=='Mensal':
        return comp330
    if value=='Anual':
        return comp3ano
@app.callback(Output('G2','figure'),
             Input('botao','value'))
def update_comp6(value):
    if value=='Semanal':
        return comp6
    if value=='Quinzena':
        return comp615
    if value=='Mensal':
        return comp630
    if value=='Anual':
        return comp6ano

@app.callback(Output('G3','figure'),
             Input('botao','value'))
def update_comp9(value):
    if value=='Semanal':
        return comp9
    if value=='Quinzena':
        return comp915
    if value=='Mensal':
        return comp930
    if value=='Anual':
        return comp9ano

@app.callback(Output('G4','figure'),
             Input('botao','value'))
def update_comp12(value):
    if value=='Semanal':
        return comp12
    if value=='Quinzena':
        return comp1215
    if value=='Mensal':
        return comp1230
    if value=='Anual':
        return comp12ano

@app.callback(Output('G5','figure'),
             Input('botao','value'))
def update_comp15(value):
    if value=='Semanal':
        return comp15
    if value=='Quinzena':
        return comp1515
    if value=='Mensal':
        return comp1530
    if value=='Anual':
        return comp15ano

@app.callback(Output('G6','figure'),
             Input('botao','value'))
def update_comp18(value):
    if value=='Semanal':
        return comp18
    if value=='Quinzena':
        return comp1815
    if value=='Mensal':
        return comp1830
    if value=='Anual':
        return comp18ano
@app.callback(Output('G7','figure'),
             Input('botao','value'))
def update_comp21(value):
    if value=='Semanal':
        return comp21
    if value=='Quinzena':
        return comp2115
    if value=='Mensal':
        return comp2130
    if value=='Anual':
        return comp21ano

@app.callback(Output('G8','figure'),
             Input('botao','value'))
def update_vxi(value):
    if value=='Semanal':
        return vxi
    if value=='Quinzena':
        return vxi15
    if value=='Mensal':
        return vxi30
    if value=='Anual':
        return vxiano

@app.callback(Output('G9','figure'),
             Input('botao','value'))
def update_VC(value):
    if value=='Semanal':
        return VC
    if value=='Quinzena':
        return VC15
    if value=='Mensal':
        return VC30
    if value=='Anual':
        return VCano

@app.callback(Output('G10','figure'),
             Input('botao','value'))
def update_diacanal(value):
    if value=='Semanal':
        return diacanal
    if value=='Quinzena':
        return diacanal15
    if value=='Mensal':
        return diacanal30
    if value=='Anual':
        return diacanalano

@app.callback(Output('G11','figure'),
             Input('botao','value'))
def update_perfgeral(value):
    if value=='Semanal':
        return perfgeral
    if value=='Quinzena':
        return perfgeral15
    if value=='Mensal':
        return perfgeral30
    if value=='Anual':
        return perfgeralano
@app.callback(Output('G12','figure'),
             Input('botao','value'))
def update_grafest1(value):
    if value=='Semanal':
        return grafest1
    if value=='Quinzena':
        return grafest115
    if value=='Mensal':
        return grafest130
    if value=='Anual':
        return grafest1ano

@app.callback(Output('G13','figure'),
             Input('botao','value'))
def update_grafest2(value):
    if value=='Semanal':
        return grafest2
    if value=='Quinzena':
        return grafest215
    if value=='Mensal':
        return grafest230
    if value=='Anual':
        return grafest2ano

@app.callback(Output('G14','figure'),
             Input('botao','value'))
def update_grafest3(value):
    if value=='Semanal':
        return grafest3
    if value=='Quinzena':
        return grafest315
    if value=='Mensal':
        return grafest330
    if value=='Anual':
        return grafest3ano

@app.callback(Output('G15','figure'),
             Input('botao','value'))
def update_grafest4(value):
    if value=='Semanal':
        return grafest4
    if value=='Quinzena':
        return grafest415
    if value=='Mensal':
        return grafest430
    if value=='Anual':
        return grafest4ano


# RODANDO
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8050)) 
    app.run_server(debug=True, host="0.0.0.0", port=port)
