import filecmp
import pytest
import os

def read_file(file_path):
    """Lit le contenu d'un fichier et renvoie une liste de lignes."""
    with open(file_path, 'r') as f:
        return f.readlines()

def compare_content(file1_lines, file2_lines):
    """
    Compare deux fichiers ligne par ligne et colonne par colonne.
    Retourne un dictionnaire avec chaque clé et ses valeurs suivies du statut 'OK' ou 'KO'.
    """
    results = {}
    
    # Vérifier que les deux fichiers ont le même nombre de lignes
    assert len(file1_lines) == len(file2_lines), (
        f"Les fichiers ont un nombre de lignes différent : {len(file1_lines)} vs {len(file2_lines)}"
    )
    
    # Comparer ligne par ligne
    for i, (line1, line2) in enumerate(zip(file1_lines, file2_lines), 1):
        columns1 = line1.strip().split()
        columns2 = line2.strip().split()
        
        # Vérifier que chaque ligne a le même nombre de colonnes
        assert len(columns1) == len(columns2), (
            f"Différence dans le nombre de colonnes à la ligne {i}:\n{file1_lines[i-1]} vs {file2_lines[i-1]}"
        )
        
        # Comparer colonne par colonne
        for j, (col1, col2) in enumerate(zip(columns1, columns2)):
            column_key = f"Ligne {i} Colonne {j + 1}"
            if col1 != col2:
                # Afficher col1 à la place de l'indice pour le message
                results[column_key] = f'{col1} - {col2}:ko'
            else:
                results[column_key] = f'{col1}:ok'
    
    return results

@pytest.fixture(scope='module')
def files():
    """Renvoie les chemins des fichiers à tester."""
    # Chemin du fichier 1
    file1 = '/home/amine/dev/test-compare-file/file1.txt'
    file2 = '/home/amine/dev/test-compare-file/file2.txt'
    return file1, file2

def test_files_exist(files):
    """Teste si les fichiers existent."""
    file1, file2 = files
    
    # Affiche les chemins des fichiers pour le débogage
    print(f"Fichier 1: {file1}, Fichier 2: {file2}")
    
    # Vérifiez que les fichiers existent avant de les lire
    assert os.path.exists(file1), f"Le fichier {file1} n'existe pas."
    assert os.path.exists(file2), f"Le fichier {file2} n'existe pas."

def test_shallow_comparison(files):
    """Teste si les fichiers sont identiques via une comparaison simple (shallow)."""
    file1, file2 = files
    
    # Comparaison simple avec filecmp (shallow comparison)
    shallow_result = filecmp.cmp(file1, file2, shallow=False)
    assert shallow_result, f"Les fichiers {file1} et {file2} sont différents."

def test_detailed_comparison(files):
    """Compare les fichiers avec une vérification ligne par ligne et colonne par colonne."""
    file1, file2 = files
    
    # Lire le contenu des fichiers
    content_file1 = read_file(file1)
    content_file2 = read_file(file2)
    
    # Comparaison ligne par ligne et colonne par colonne
    detailed_result = compare_content(content_file1, content_file2)
    
    # Affichage des résultats détaillés
    for line, comparison in detailed_result.items():
        print(f'{line}: {comparison}')
    
    # Vérifier les différences
    differences_found = any('ko' in result for result in detailed_result.values())
    assert not differences_found, f"Les fichiers {file1} et {file2} ont des différences : {detailed_result}"

