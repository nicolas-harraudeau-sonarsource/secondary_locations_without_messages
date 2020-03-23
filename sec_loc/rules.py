from client import Client
from constants import URL, token
import json
import logging
import http.client as http_client

# http_client.HTTPConnection.debuglevel = 1

# You must initialize logging, otherwise you'll not see debug output.
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True

def get_issues(max, language):
    client = Client(base_url=URL, token=token)
    # for lang_response in client.get("api/languages/list"):
    #     for language in lang_response["languages"]:
            # for rules_response in client.get("api/rules/search", languages=language["key"]):
    
    issues = []
    for rules_response in client.get("api/rules/search", languages=language):
        for rule in rules_response["rules"]:
            # print("rule", rule["key"])
            print(".", end ="", flush=True)
            for issues_response in client.get("api/issues/search", rules=rule["key"], page_size=2, pages=2):
                if issues_response["issues"]:
                    issues.append(issues_response["issues"][0])
                    # print(f"nb issues: {len(issues)}")
                    if len(issues) > max:
                        print()
                        return issues
    print()
    return issues

def aggregate_language_stats(language, issues):
    rules_with_messages = {}
    rules_without_messages = {}
    rules_without_secondary = {}
    for issue in issues:
        url = f"https://peach.sonarsource.com/project/issues?id={issue['project']}&issues={issue['key']}"
        if issue["flows"] and issue["flows"][0]["locations"]:
            location = issue["flows"][0]["locations"][0]
            if "msg" in location:
                rules_with_messages[issue["rule"]] = dict(
                    message = location["msg"],
                    url=url
                )
            else:
                rules_without_messages[issue["rule"]] = dict(
                    url=url
                )

        else:
            rules_without_secondary[issue["rule"]] = dict(
                url=url
            )
    print("Language:", language)
    print("with messages", len(rules_with_messages))
    print("without messages", len(rules_without_messages))
    print("no secondary", len(rules_without_secondary))

    print(json.dumps(rules_without_messages, sort_keys=True, indent=4))
# result = client.get("api/rules/search")
# print(json.dumps(result, sort_keys=True, indent=4))


for language in ["java"]:
    issues = get_issues(600, language)
    aggregate_language_stats(language, issues)