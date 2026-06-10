from Bio import Entrez

Entrez.email = "imkiruba2005@gmail.com"


def search_pubmed(query, max_results=5):
    handle = Entrez.esearch(
        db="pubmed",
        term=query,
        retmax=max_results,
        sort="relevance"
    )

    record = Entrez.read(handle)
    ids = record["IdList"]

    if not ids:
        return []

    handle = Entrez.esummary(
        db="pubmed",
        id=",".join(ids)
    )

    summaries = Entrez.read(handle)

    papers = []

    for item in summaries:
        papers.append({
            "pmid": item.get("Id", ""),
            "title": item.get("Title", "No title available"),
            "journal": item.get("FullJournalName", "Unknown journal"),
            "pub_date": item.get("PubDate", "Unknown date")
        })

    return papers


def get_pubmed_context(query, max_results=5):
    papers = search_pubmed(query, max_results)

    if not papers:
        return ""

    context = ""

    for paper in papers:
        context += f"""
PMID: {paper['pmid']}
Title: {paper['title']}
Journal: {paper['journal']}
Publication Date: {paper['pub_date']}
"""

    return context


if __name__ == "__main__":
    query = input("Enter PubMed query: ")

    papers = search_pubmed(query)

    if not papers:
        print("No PubMed results found.")
    else:
        print("\nPubMed Papers:\n")

        for i, paper in enumerate(papers, start=1):
            print(f"{i}. {paper['title']}")
            print(f"PMID: {paper['pmid']}")
            print(f"Journal: {paper['journal']}")
            print(f"Date: {paper['pub_date']}")
            print("-" * 50)