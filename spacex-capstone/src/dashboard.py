from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
import pandas as pd,folium,math,json
from folium.plugins import MarkerCluster,MousePosition
from dash import Dash,dcc,html,Input,Output
import plotly.express as px
G=pd.read_csv(str(ROOT/'data/spacex_launch_geo.csv'));D=pd.read_csv(str(ROOT/'data/spacex_launch_dash.csv')); sites=G.groupby('Launch Site',as_index=False).first()
m=folium.Map(location=[30,-98],zoom_start=4,tiles='OpenStreetMap')
for _,r in sites.iterrows():
 folium.CircleMarker([r.Lat,r.Long],radius=8,color='#0b49cb',fill=True,tooltip=r['Launch Site'],popup=f"{r['Launch Site']}: {r.Lat:.5f}, {r.Long:.5f}").add_to(m)
 folium.Marker([r.Lat,r.Long],icon=folium.DivIcon(icon_anchor=(-10, {'CCAFS LC-40':-20,'CCAFS SLC-40':-45,'KSC LC-39A':5,'VAFB SLC-4E':0}[r['Launch Site']]),html=f'<div style="font: bold 15px Arial;width:160px;background:white">{r["Launch Site"]}</div>')).add_to(m)
m.save(str(ROOT/'results/map1.html'))
m=folium.Map(location=[28.565,-80.60],zoom_start=12,tiles='OpenStreetMap');cluster=MarkerCluster().add_to(m)
for _,r in G.iterrows():folium.Marker([r.Lat,r.Long],tooltip=f"Flight {r['Flight Number']} | Class {r['class']}",icon=folium.Icon(color='green' if r['class'] else 'red',icon='info-sign')).add_to(cluster)
MousePosition().add_to(m);m.save(str(ROOT/'results/map2.html'))
pad=[28.562302,-80.577356];points={'Coastline (sample point)':[28.5637,-80.5679],'Road (sample point)':[28.5632,-80.5817],'Rail corridor (sample point)':[28.5720,-80.5865]}
def km(a,b):
 p1,p2=map(math.radians,[a[0],b[0]]);dp=p2-p1;dl=math.radians(b[1]-a[1]);return 6371*2*math.asin(math.sqrt(math.sin(dp/2)**2+math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2))
m=folium.Map(location=pad,zoom_start=14,tiles='OpenStreetMap');folium.Marker(pad,tooltip='CCAFS LC-40').add_to(m)
for name,pt in points.items():
 dist=km(pad,pt);folium.PolyLine([pad,pt],color='#0b49cb',weight=3).add_to(m);folium.Marker(pt,icon=folium.DivIcon(icon_anchor=({'Coastline (sample point)':(-5,0),'Road (sample point)':(220,-35),'Rail corridor (sample point)':(100,40)}[name]),html=f'<div style="font:14px Arial;background:white;width:200px">{name}<br>{dist:.2f} km straight line</div>')).add_to(m)
m.save(str(ROOT/'results/map3.html'));print({k:km(pad,v) for k,v in points.items()})
app=Dash(__name__);app.layout=html.Div([html.H2('SpaceX launch outcomes'),html.P('Reconstructed dashboard using IBM course data, 56 records'),dcc.Dropdown(['ALL']+sorted(D['Launch Site'].unique().tolist()),'ALL',id='site',clearable=False),html.Div([dcc.Graph(id='pie'),dcc.Graph(id='scatter')],style={'display':'grid','gridTemplateColumns':'1fr 1.4fr'}),html.Label('Payload mass range (kg)'),dcc.RangeSlider(0,10000,100,value=[0,10000],id='mass',marks={i:str(i) for i in range(0,10001,2000)})],style={'fontFamily':'Arial','padding':'20px'})
@app.callback(Output('pie','figure'),Output('scatter','figure'),Input('site','value'),Input('mass','value'))
def update(site,mass):
 d=D if site=='ALL' else D[D['Launch Site']==site]
 if site=='ALL':
  p=d.groupby('Launch Site',as_index=False)['class'].sum();pie=px.pie(p,names='Launch Site',values='class',title='Share of successful outcomes by site')
 else:
  p=d['class'].value_counts().rename_axis('Class').reset_index(name='Count');p['Class']=p.Class.map({0:'Class 0',1:'Class 1'});pie=px.pie(p,names='Class',values='Count',title=f'{site}: outcome ratio')
 dd=d[d['Payload Mass (kg)'].between(*mass)]
 scatter=px.scatter(dd,x='Payload Mass (kg)',y='class',color='Booster Version Category',hover_data=['Launch Site'],title=f'Payload {mass[0]:,}–{mass[1]:,} kg: {len(dd)} launches')
 scatter.update_yaxes(tickvals=[0,1]);return pie,scatter
if __name__=='__main__':app.run(port=8050,debug=False)
