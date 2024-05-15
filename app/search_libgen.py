from libgen_api_enhanced import LibgenSearch
import eel 

search = LibgenSearch()

@eel.expose
def title_search(query):
    
    results = search.search_title(query)
    
    return results