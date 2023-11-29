import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

csv_url = 'https://docs.google.com/spreadsheets/d/1mVyF0KOBIEe1RJNcDGp0VXMo_d9XPExGX3MT2EqVRzk/gviz/tq?tqx=out:csv&sheet=0'

# Use pandas to read the CSV file directly from the Google Sheets public URL
data = pd.read_csv(csv_url)

mean_values = data.drop(columns=["Carimbo de data/hora"]).mean()
mean_df = pd.DataFrame(mean_values, columns=['Média']).reset_index()
mean_df.rename(columns={'index': 'Nome'}, inplace=True)
mean_df['Nome'] = mean_df['Nome'].str.replace('\[', '', regex=True).str.replace('\]', '', regex=True)
mean_df_sorted = mean_df.sort_values('Média', ascending=True)
mean_df_sorted['Ranking'] = range(len(mean_df_sorted), 0, -1)

st.title('Craque do Perebas')
fig, ax = plt.subplots()
for spine in ax.spines.values():
    spine.set_visible(False)

ax.set_facecolor('none')
fig.patch.set_facecolor('none')

bars = ax.barh(mean_df_sorted['Nome'], mean_df_sorted['Média'], color='yellow')
ax.set_title('Média das Avaliações por Nome', color='white')

ax.set_yticklabels(mean_df_sorted['Nome'], va='center', ha='left', position=(-0.21,0))

for bar, ranking in zip(bars, mean_df_sorted['Ranking']):
    width = bar.get_width()
    label_x_pos_media = width + 0.02  # Posição do valor da média para o fim da barra
    label_y_pos = bar.get_y() + bar.get_height() / 2
    ax.text(label_x_pos_media, label_y_pos, f'{width:.2f}', va='center', color='white')
    ax.text(-1.25, label_y_pos, f'{ranking}º', va='center', ha='left', color='white')

ax.set_xticks([])

ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')

ax.yaxis.set_ticks_position('none')

ax.grid(False)

st.pyplot(fig, transparent=True)

