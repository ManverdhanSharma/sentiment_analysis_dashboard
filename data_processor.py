import pandas as pd
import io
import json
from datetime import datetime

class DataProcessor:
    def __init__(self):
        self.supported_formats = ['csv', 'txt', 'json']
    
    def process_uploaded_file(self, uploaded_file):
        """Process uploaded file and extract text data"""
        try:
            file_extension = uploaded_file.name.split('.')[-1].lower()
            
            if file_extension == 'csv':
                return self.process_csv(uploaded_file)
            elif file_extension == 'txt':
                return self.process_txt(uploaded_file)
            elif file_extension == 'json':
                return self.process_json(uploaded_file)
            else:
                raise ValueError(f"Unsupported file format: {file_extension}")
                
        except Exception as e:
            raise Exception(f"Error processing file: {str(e)}")
    
    def process_csv(self, uploaded_file):
        """Process CSV file"""
        df = pd.read_csv(uploaded_file)
        
        # Try to find text columns
        text_columns = []
        for col in df.columns:
            if df[col].dtype == 'object':  # String columns
                # Check if column contains substantial text
                avg_length = df[col].astype(str).str.len().mean()
                if avg_length > 10:  # Assume text if average length > 10 chars
                    text_columns.append(col)
        
        if not text_columns:
            raise ValueError("No text columns found in CSV file")
        
        # Use the first text column
        text_column = text_columns[0]
        texts = df[text_column].dropna().astype(str).tolist()
        
        return {
            'texts': texts,
            'metadata': {
                'source': 'CSV file',
                'total_rows': len(df),
                'text_column': text_column,
                'available_columns': text_columns
            }
        }
    
    def process_txt(self, uploaded_file):
        """Process text file"""
        content = uploaded_file.read().decode('utf-8')
        
        # Split by lines and filter empty lines
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        
        return {
            'texts': lines,
            'metadata': {
                'source': 'Text file',
                'total_lines': len(lines)
            }
        }
    
    def process_json(self, uploaded_file):
        """Process JSON file"""
        content = uploaded_file.read().decode('utf-8')
        data = json.loads(content)
        
        texts = []
        
        if isinstance(data, list):
            # Array of objects or strings
            for item in data:
                if isinstance(item, str):
                    texts.append(item)
                elif isinstance(item, dict):
                    # Try to find text fields
                    for key, value in item.items():
                        if isinstance(value, str) and len(value) > 10:
                            texts.append(value)
                            break
        elif isinstance(data, dict):
            # Single object - extract text values
            for key, value in data.items():
                if isinstance(value, str) and len(value) > 10:
                    texts.append(value)
        
        return {
            'texts': texts,
            'metadata': {
                'source': 'JSON file',
                'total_texts': len(texts)
            }
        }
    
    def export_results_csv(self, results, summary_stats):
        """Export analysis results to CSV format"""
        # Create DataFrame from results
        df_data = []
        for result in results:
            df_data.append({
                'text': result['original_text'],
                'sentiment': result['sentiment'],
                'confidence': result['confidence'],
                'intensity': result['intensity'],
                'emotions': ', '.join(result['emotions']),
                'key_phrases': ', '.join(result['key_phrases']),
                'analyzed_at': result['analyzed_at']
            })
        
        df = pd.DataFrame(df_data)
        
        # Add summary stats as comments
        summary_text = f"""
# Sentiment Analysis Results
# Generated on: {datetime.now().isoformat()}
# Total Analyzed: {summary_stats.get('total_analyzed', 0)}
# Positive: {summary_stats.get('positive_percentage', 0)}%
# Negative: {summary_stats.get('negative_percentage', 0)}%
# Neutral: {summary_stats.get('neutral_percentage', 0)}%
# Average Confidence: {summary_stats.get('average_confidence', 0)}
# Average Intensity: {summary_stats.get('average_intensity', 0)}
"""
        
        # Convert to CSV
        output = io.StringIO()
        output.write(summary_text)
        df.to_csv(output, index=False)
        
        return output.getvalue()
    
    def export_results_json(self, results, summary_stats):
        """Export analysis results to JSON format"""
        export_data = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'total_analyzed': len(results),
                'summary_stats': summary_stats
            },
            'results': results
        }
        
        return json.dumps(export_data, indent=2)
    
    def create_sample_data(self):
        """Create sample data for testing"""
        sample_texts = [
            "I absolutely love this product! It's amazing and works perfectly.",
            "This is the worst purchase I've ever made. Completely disappointed.",
            "The product is okay, nothing special but does what it's supposed to do.",
            "Outstanding quality and excellent customer service. Highly recommended!",
            "Terrible experience. The product broke after just one day.",
            "Good value for money. I'm satisfied with my purchase.",
            "Not what I expected. The description was misleading.",
            "Fantastic! Exceeded all my expectations. Will buy again.",
            "Average product. It works but could be better.",
            "Excellent build quality and fast shipping. Very happy!"
        ]
        
        return {
            'texts': sample_texts,
            'metadata': {
                'source': 'Sample data',
                'total_texts': len(sample_texts)
            }
        }
