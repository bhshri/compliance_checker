from openai import OpenAI
from trafilatura import extract, fetch_url
import ast

OPENAI_API_KEY = '[INSERT_OPENAI_KEY_HERE]'
MODEL_NAME = "gpt-4-1106-preview"

COMPLIANCE_POLICY_URL = "https://stripe.com/docs/treasury/marketing-treasury"

SYSTEM_MESSAGE = "You are expert at reviewing financial and marketing documents and identifying problems based on regulations and rules and inform about the non compliance."
INSTRUCTION_TEMPLATE = """Leverage the rules, regulations and terms provided in the compliance policy to evaluate the webpage content and provide the non complaint results.
Compliance Policy:\ncompliance_policy\nWebpage Content:\nwebpage_content\nGive all the non compliant content(phrases/sentences from the webpage content) and the detailed explanation/reason (based on compliance policy). Think step by step.
Use the JSON format shown below
{
  "NonCompliantContent": [
    {
      "Content": "...",
      "Reason": "..."
    },
    {
      "Content": "...",
      "Reason": "..."
    }
    ]
}
"""

class ComplianceChecker:
    def __init__(self) -> None:
        self.client = OpenAI(api_key = OPENAI_API_KEY)
        self.compliance_policy = self.__extract_text_from_webpage(COMPLIANCE_POLICY_URL)

    def __extract_text_from_webpage(self,webpage_url):
        document = fetch_url(webpage_url)
        webpage_content = extract(document)
        return webpage_content
    
    def get_noncompliant_results(self,webpage_url):
        webpage_content = self.__extract_text_from_webpage(webpage_url)
        instruction = INSTRUCTION_TEMPLATE.replace("compliance_policy",self.compliance_policy).replace("webpage_content",webpage_content)
        completion = self.client.chat.completions.create(model=MODEL_NAME,
                                                        messages=[{"role": "system", "content": SYSTEM_MESSAGE},
                                                                  {"role": "user", "content": instruction}],
                                                        temperature= 0, 
                                                        response_format={ "type": "json_object" })
        return ast.literal_eval(completion.choices[0].message.content)
    

if __name__ == "__main__":
    complaince_checker = ComplianceChecker()
    print(complaince_checker.get_noncompliant_results('https://www.joinguava.com/'))


