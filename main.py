import json
import re
from typing import List, Optional

from anthropic import Anthropic
from pydantic import BaseModel, Field


class Expression(BaseModel):
    phrase: str = Field(description="The extracted phrase or expression")
    timestamp: str = Field(description="Timestamp in the format MM:SS")
    meaning: str = Field(description="Definition or meaning in context")
    context: str = Field(description="The original sentence where it appeared")
    example: str = Field(description="A new example sentence")
    type: str = Field(description="Type of expression (idiom/political term/formal/etc)")
    level: str = Field(description="Difficulty level (intermediate/advanced/native)")


class SRTVocabExtractor:
    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)

    def parse_srt_timestamps(self, srt_content: str) -> List[tuple]:
        """Extract text with timestamps from SRT file"""
        pattern = r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.*?)(?=\n\d+\n|$)'
        matches = re.finditer(pattern, srt_content, re.DOTALL)
        return [(match.group(1), match.group(3).strip()) for match in matches]

    def create_analysis_prompt(self, text_segment: str, timestamp: str) -> str:
        return f"""Please analyze this text segment and identify ONE significant advanced expression, idiom, or notable vocabulary. 
        Provide the analysis in JSON format with these exact fields:
        - phrase: the expression itself
        - timestamp: {timestamp}
        - meaning: clear definition
        - context: how it's used in the original text
        - example: a new example sentence
        - type: category (idiom/political term/formal/etc)
        - level: difficulty level (intermediate/advanced/native)

        Text segment:
        {text_segment}

        Respond with only the JSON object, no other text.
        """

    def analyze_segment(self, text: str, timestamp: str) -> Optional[Expression]:
        """Analyze a single text segment using Claude"""
        try:
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                temperature=0,
                system="You are an expert in English language analysis, focusing on advanced vocabulary and expressions.",
                messages=[{
                    "role": "user",
                    "content": self.create_analysis_prompt(text, timestamp)
                }]
            )

            # Parse JSON response
            response_content = message.content[0].text
            expression_dict = json.loads(response_content)
            return Expression(**expression_dict)

        except Exception as e:
            print(f"Error analyzing segment at {timestamp}: {e}")
            return None

    def process_srt_file(self, srt_content: str) -> List[Expression]:
        """Process entire SRT file and extract expressions"""
        segments = self.parse_srt_timestamps(srt_content)
        expressions = []

        for index, (timestamp, text) in enumerate(segments, start=1):
            print(f"Analyzing segment {index}/{len(segments)} at {timestamp}: {text}")
            if result := self.analyze_segment(text, timestamp):
                expressions.append(result)

        return expressions

    def generate_markdown_report(self, expressions: List[Expression]) -> str:
        """Generate a formatted markdown report of findings"""
        markdown = "# Advanced Expression Analysis Report\n\n"

        # Group expressions by type
        expressions_by_type = {}
        for expr in expressions:
            if expr.type not in expressions_by_type:
                expressions_by_type[expr.type] = []
            expressions_by_type[expr.type].append(expr)

        # Generate report by type
        for expr_type, expr_list in expressions_by_type.items():
            markdown += f"## {expr_type.title()} Expressions\n\n"
            for expr in expr_list:
                markdown += f"### {expr.phrase}\n"
                markdown += f"- **Timestamp:** {expr.timestamp}\n"
                markdown += f"- **Level:** {expr.level}\n"
                markdown += f"- **Meaning:** {expr.meaning}\n"
                markdown += f"- **Context:** _{expr.context}_\n"
                markdown += f"- **Example:** _{expr.example}_\n\n"

        return markdown


def process_news_transcript(api_key: str, srt_file_path: str, output_path: str):
    """Main function to process a news transcript"""
    extractor = SRTVocabExtractor(api_key)

    # Read SRT file
    with open(srt_file_path, "r", encoding="utf-8") as f:
        srt_content = f.read()

    # Process content
    print("Processing transcript...")
    expressions = extractor.process_srt_file(srt_content)
    print(f"Found {len(expressions)} advanced expressions.")

    # Generate and save report
    print("Generating report...")
    report = extractor.generate_markdown_report(expressions)

    # create the results directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)

    return f"Analysis complete. Report saved to {output_path}"


# Usage example:
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")

    result = process_news_transcript(
        api_key=api_key,
        srt_file_path="data/srt_sample.srt",
        output_path="results/srt_report.md"
    )
    print(result)
