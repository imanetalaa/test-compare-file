import filecmp
import pytest
import os
 
def read_file(file_path):
    """Lit le contenu d'un fichier et renvoie une liste de lignes."""
    with open(file_path, 'r') as f:
        return f.readlines()

# def compare_content(file1_lines, file2_lines):
#     """
#     Compare deux fichiers ligne par ligne et colonne par colonne.
#     Retourne un dictionnaire avec chaque clé et ses valeurs suivies du statut 'OK' ou 'KO'.
#     """
#     results = {}

#     # Vérifier que les deux fichiers ont le même nombre de lignes
#     assert len(file1_lines) == len(file2_lines), (
#         f"Les fichiers ont un nombre de lignes différent : {len(file1_lines)} vs {len(file2_lines)}"
#     )

#     # Comparer ligne par ligne
#     for i, (line1, line2) in enumerate(zip(file1_lines, file2_lines), 1):
#         columns1 = line1.strip().split()
#         columns2 = line2.strip().split()

#         # Vérifier que chaque ligne a le même nombre de colonnes
#         assert len(columns1) == len(columns2), (
#             f"Différence dans le nombre de colonnes à la ligne {i}:\n{file1_lines[i-1]} vs {file2_lines[i-1]}"
#         )

#         # Comparer colonne par colonne
#         for j, (col1, col2) in enumerate(zip(columns1, columns2)):
#             column_key = f"Ligne {i} Colonne {j+1}"
#             if col1 != col2:
#                 results[column_key] = f'{col1}:ko vs {col2}:ko'
#             else:
#                 results[column_key] = f'{col1}:ok'

#     return results

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
        previous_col_value = None  # pour stocker la valeur de la colonne précédente
        for j, (col1, col2) in enumerate(zip(columns1, columns2)):
            column_key = f"Ligne {i} Colonne {j + 1}"
            
            # Si nous avons une valeur précédente, l'utiliser dans le message d'erreur
            if previous_col_value is not None and col1 != col2:
                results[column_key] = f'{previous_col_value} - {col1} - {col2}:ko'
            else:
                # On stocke la valeur actuelle pour la prochaine itération
                if col1 != col2:
                    results[column_key] = f'- {col1} - {col2}:ko'
                else:
                    results[column_key] = f'{col1}:ok'
                    
            # Mettre à jour la valeur précédente pour la prochaine itération
            previous_col_value = col1  # mise à jour avec la colonne actuelle
    
    return results
 
@pytest.fixture(scope='module')
def files():
    """Renvoie les chemins des fichiers à tester."""
    # Chemin du fichier 1
    file1 = os.environ.get('RO')  # Chemin du premier fichier à tester
    file2 = os.environ.get('RP')  # Chemin du second fichier à tester
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

    # Création d'un message de rapport formaté
    report_lines = []
    
    # Variable pour stocker la valeur précédente de la colonne
    previous_col_value = None
    
    for line, comparison in detailed_result.items():
        # Ajout de la logique pour inclure la valeur de la colonne précédente en cas de différence
        report_lines.append(f'{line}: {comparison}')
        if 'ko' in comparison:
            if previous_col_value is not None:
                report_lines[-1] = f'{previous_col_value} - {comparison}'
        # Mise à jour de la valeur précédente pour la prochaine ligne
        previous_col_value = comparison

    # Joindre toutes les lignes pour le rapport
    report_message = "\n".join(report_lines)
    
    # Afficher le message dans la sortie standard (ou l'envoyer à Xray)
    print(report_message)
    
    # Vérifier les différences
    differences_found = any('ko' in result for result in detailed_result.values())
    assert not differences_found, f"Les fichiers {file1} et {file2} ont des différences :\n{report_message}"


# def test_detailed_comparison(files):
#     """Compare les fichiers avec une vérification ligne par ligne et colonne par colonne."""
#     file1, file2 = files

#     # Lire le contenu des fichiers
#     content_file1 = read_file(file1)
#     content_file2 = read_file(file2)

#     # Comparaison ligne par ligne et colonne par colonne
#     detailed_result = compare_content(content_file1, content_file2)

#     # Création d'un message de rapport formaté
#     report_lines = []
#     for line, comparison in detailed_result.items():
#         report_lines.append(f'{line}: {comparison}')

#     # Joindre toutes les lignes pour le rapport
#     report_message = "\n".join(report_lines)
#     # Afficher le message dans la sortie standard (ou l'envoyer à Xray)
#     print(report_message)
#     # Vérifier les différences
#     differences_found = any('ko' in result for result in detailed_result.values())
#     assert not differences_found, f"Les fichiers {file1} et {file2} ont des différences :\n{report_message}"

def test_column_comparisons(files):
    """Test chaque colonne pour les différences."""
    file1, file2 = files

    # Lire le contenu des fichiers
    content_file1 = read_file(file1)
    content_file2 = read_file(file2)

    detailed_result = compare_content(content_file1, content_file2)

    # Vérifiez chaque ligne et colonne individuellement
    for key, result in detailed_result.items():
        if 'ko' in result:
            assert False, f"Différence trouvée dans {key}: {result}"

def test_columns_comparisons(files):
    """Test chaque colonne pour afficher uniquement les différences."""
    file1, file2 = files

    # Lire le contenu des fichiers
    content_file1 = read_file(file1)
    content_file2 = read_file(file2)

    # Comparaison ligne par ligne et colonne par colonne
    detailed_result = compare_content(content_file1, content_file2)

    # Filtrer uniquement les différences avec "ko"
    ko_results = {key: value for key, value in detailed_result.items() if 'ko' in value}

    # Vérifiez chaque colonne individuellement et affichez uniquement les différences
    assert not ko_results, (
        f"Des différences existent dans les colonnes :\n"
        + "\n".join([f"{key}: {value}" for key, value in ko_results.items()])
    )


