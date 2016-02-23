import urllib2
import time
import re
from bs4 import BeautifulSoup
from fuzzywuzzy import process, fuzz
from jinja2 import Template
import codecs
import random

USER_AGENTS = ["Mozilla/5.0"]

def get_candidate_soup(candidate):
    if candidate == "hillary":
        hillary_issues_url = "https://www.hillaryclinton.com/issues/"
        hillary_html = urllib2.urlopen(urllib2.Request(hillary_issues_url, headers={ 'User-Agent': random.choice(USER_AGENTS) })).read()
        hillary_soup = BeautifulSoup(hillary_html, "html.parser")
        return hillary_soup
    if candidate == "bernie":
        bernie_issues_url = "https://berniesanders.com/issues/"
        # old Bernie takes some finagling
        bernie_html = urllib2.urlopen(urllib2.Request(bernie_issues_url, headers={ 'User-Agent': random.choice(USER_AGENTS) })).read()
        bernie_soup = BeautifulSoup(bernie_html, "html.parser")
        return bernie_soup
    # if we reached this point there's an issue
    raise ValueError("candidate not supported")

def get_issues(hillary_soup, bernie_soup):
    # I know this is ugly, but the issues don't belong to any specific class, and
    # it seems the easiest way to find them is by their font size.
    hillary_issues_html = hillary_soup.find_all("p", {"style": re.compile(r".+1\.5em.+") })
    # Nice use of header tags, Bern. Other candidates could learn a lot from you.
    bernie_issues_html = bernie_soup.select("h3 > a")

    hillary_issues = [tag.text for tag in hillary_issues_html]
    bernie_issues = [tag.text for tag in bernie_issues_html]

    return hillary_issues, bernie_issues

def match_issues(hillary_issues, bernie_issues):
    matched_issues = []
    for hissue in hillary_issues:
        matching_bern_issue = process.extractOne(hissue, bernie_issues, scorer=fuzz.token_set_ratio, score_cutoff = 65)
        if matching_bern_issue:
            matched_issues.append((hissue, matching_bern_issue[0]))
    return matched_issues

def get_text_for_issue(hillary_soup, bernie_soup, issue_tuple):
    hillary_issue = issue_tuple[0]
    bernie_issue = issue_tuple[1]
    hillary_text = get_text_for_hillary_issue(hillary_soup, hillary_issue)
    bernie_text = get_text_for_bernie_issue(bernie_soup, bernie_issue)
    return hillary_text, bernie_text

def get_text_for_hillary_issue(hillary_soup, issue):
    issue_tag = hillary_soup.find("p", text=issue)
    link_tag = issue_tag.find_next("a", text="Read more")
    bullet_points = extract_bullet_points_from_url(link_tag["href"])
    return bullet_points

def get_text_for_bernie_issue(bernie_soup, issue):
    link_tag = bernie_soup.find("a", text=issue)
    bullet_points = extract_bullet_points_from_url(link_tag["href"])
    return bullet_points

def extract_bullet_points_from_url(url):
    print url
    soup = BeautifulSoup(urllib2.urlopen(urllib2.Request(url, headers={ 'User-Agent': random.choice(USER_AGENTS) })).read(), "html.parser")
    bullet_points = soup.find_all("li")
    text_points = [point.text.replace("\n", "") for point in bullet_points]
    text_points = [t for t in text_points if len(t.split()) > 5 and "Follow" not in t]
    return text_points

if __name__ == "__main__":
    hillary_soup = get_candidate_soup("hillary")
    bernie_soup = get_candidate_soup("bernie")
    hillary_issues, bernie_issues = get_issues(hillary_soup, bernie_soup)
    matched_issues = match_issues(hillary_issues, bernie_issues)
    issues_template = Template(open("issues_we_found.md.template").read())
    issues_text = issues_template.render(hillary_issues=hillary_issues, bernie_issues=bernie_issues, matched_issues=matched_issues)
    with codecs.open("issues_we_found.md", "w", "utf-8") as issues_we_found:
        issues_we_found.write(issues_text)
    for issue in matched_issues:
        issue_template = Template(open("issue_comparison.md.template").read())
        hillary_text, bernie_text = get_text_for_issue(hillary_soup, bernie_soup, issue)
        hillary_text = "<ul><li>" + "</li><li>".join(hillary_text) + "</li></ul>"
        bernie_text = "<ul><li>" + "</li><li>".join(bernie_text) + "</li></ul>"
        with codecs.open(issue[0].split()[0] + ".md", "w", "utf-8") as specific_issue:
            specific_issue.write(issue_template.render(hillary_text=hillary_text, bernie_text=bernie_text))
        time.sleep(15) # Be kind, take time.
