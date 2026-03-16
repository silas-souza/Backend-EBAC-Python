<<<<<<< HEAD
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Carregar os dados
try:
    df = pd.read_csv('movies.csv')
except FileNotFoundError:
    print("Erro: O arquivo movies.csv não foi encontrado!")
    exit()

# 2. Limpeza básica
# Converte notas para números (N/A vira NaN) e remove os sem nota para o gráfico
df['Nota'] = pd.to_numeric(df['Nota'], errors='coerce')
df_grafico = df.dropna(subset=['Nota']).sort_values(by='Nota', ascending=False)

# 3. Criar o gráfico
plt.figure(figsize=(12, 8))
sns.set_theme(style="whitegrid")

# Criando o gráfico de barras
plot = sns.barplot(
    x='Nota', 
    y='Titulo', 
    data=df_grafico, 
    palette='viridis',
    hue='Titulo',
    legend=False
)

# Customização técnica
plt.title('Top Filmes Populares por Avaliação (IMDb)', fontsize=16)
plt.xlabel('Nota (0-10)', fontsize=12)
plt.ylabel('Filme', fontsize=12)
plt.xlim(0, 10) # Garante que a escala vá até 10

# Adiciona o valor da nota ao lado de cada barra
for i, p in enumerate(plot.patches):
    plot.annotate(f'{p.get_width():.1f}', 
                   (p.get_width() + 0.1, p.get_y() + p.get_height()/2),
                   va='center')

plt.tight_layout()

# 4. Salvar e Mostrar
plt.savefig('grafico_filmes.png')
print("✅ Estatísticas geradas:")
print(f"- Total de filmes analisados: {len(df)}")
print(f"- Média geral de notas: {df['Nota'].mean():.2f}")
print(f"- Anos encontrados: {df['Data'].unique()}")
print("\n🚀 Gráfico salvo como 'grafico_filmes.png'!")
plt.show()
=======
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Carregar os dados
try:
    df = pd.read_csv('movies.csv')
except FileNotFoundError:
    print("Erro: O arquivo movies.csv não foi encontrado!")
    exit()

# 2. Limpeza básica
# Converte notas para números (N/A vira NaN) e remove os sem nota para o gráfico
df['Nota'] = pd.to_numeric(df['Nota'], errors='coerce')
df_grafico = df.dropna(subset=['Nota']).sort_values(by='Nota', ascending=False)

# 3. Criar o gráfico
plt.figure(figsize=(12, 8))
sns.set_theme(style="whitegrid")

# Criando o gráfico de barras
plot = sns.barplot(
    x='Nota', 
    y='Titulo', 
    data=df_grafico, 
    palette='viridis',
    hue='Titulo',
    legend=False
)

# Customização técnica
plt.title('Top Filmes Populares por Avaliação (IMDb)', fontsize=16)
plt.xlabel('Nota (0-10)', fontsize=12)
plt.ylabel('Filme', fontsize=12)
plt.xlim(0, 10) # Garante que a escala vá até 10

# Adiciona o valor da nota ao lado de cada barra
for i, p in enumerate(plot.patches):
    plot.annotate(f'{p.get_width():.1f}', 
                   (p.get_width() + 0.1, p.get_y() + p.get_height()/2),
                   va='center')

plt.tight_layout()

# 4. Salvar e Mostrar
plt.savefig('grafico_filmes.png')
print("✅ Estatísticas geradas:")
print(f"- Total de filmes analisados: {len(df)}")
print(f"- Média geral de notas: {df['Nota'].mean():.2f}")
print(f"- Anos encontrados: {df['Data'].unique()}")
print("\n🚀 Gráfico salvo como 'grafico_filmes.png'!")
plt.show()
>>>>>>> ab293b7 (chore: initial commit)
