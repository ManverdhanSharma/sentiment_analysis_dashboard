import streamlit as st
import pandas as pd
from datetime import datetime
import time
from sentiment_analyzer import SentimentAnalyzer
from chart_generator import ChartGenerator
from data_processor import DataProcessor

# Page configuration
st.set_page_config(
    page_title="AI Sentiment Analysis Dashboard",
    page_icon="📊",
    layout="wide"
)

@st.cache_resource
def load_analyzer():
    return SentimentAnalyzer()

@st.cache_resource
def load_chart_generator():
    return ChartGenerator()

@st.cache_resource
def load_data_processor():
    return DataProcessor()

def main():
    st.title("📊 AI Sentiment Analysis Dashboard")
    st.markdown("**Analyze emotions in text using AI - Upload files or enter text directly**")
    
    # Initialize components
    try:
        analyzer = load_analyzer()
        chart_gen = load_chart_generator()
        data_processor = load_data_processor()
    except Exception as e:
        st.error(f"❌ Failed to initialize: {e}")
        st.stop()
    
    # Sidebar
    with st.sidebar:
        st.header("🎯 How It Works")
        st.markdown("""
        **1. Input Data**
        - Upload CSV, TXT, or JSON files
        - Or enter text directly
        
        **2. AI Analysis**
        - Gemini AI analyzes sentiment
        - Detects emotions and confidence
        - Extracts key phrases
        
        **3. Visual Results**
        - Interactive charts and graphs
        - Detailed analysis reports
        - Export functionality
        """)
        
        st.header("📁 Supported Formats")
        st.markdown("""
        - **CSV**: Text in columns
        - **TXT**: Line-separated text
        - **JSON**: Text in objects
        """)
        
        if st.button("🧪 Load Sample Data"):
            st.session_state.sample_data = True
    
    # Main content tabs
    tab1, tab2, tab3 = st.tabs(["📝 Input & Analysis", "📊 Results Dashboard", "📁 Export & Reports"])
    
    with tab1:
        st.header("📝 Input Your Data")
        
        # Input method selection
        input_method = st.radio(
            "Choose input method:",
            ["Upload File", "Enter Text Directly", "Use Sample Data"]
        )
        
        texts_to_analyze = []
        metadata = {}
        
        if input_method == "Upload File":
            uploaded_file = st.file_uploader(
                "Upload your file",
                type=['csv', 'txt', 'json'],
                help="Upload CSV, TXT, or JSON files containing text to analyze"
            )
            
            if uploaded_file:
                try:
                    with st.spinner("Processing file..."):
                        processed_data = data_processor.process_uploaded_file(uploaded_file)
                        texts_to_analyze = processed_data['texts']
                        metadata = processed_data['metadata']
                    
                    st.success(f"✅ Processed {len(texts_to_analyze)} texts from {metadata['source']}")
                    
                    # Show preview
                    if texts_to_analyze:
                        st.subheader("📋 Preview")
                        preview_df = pd.DataFrame({
                            'Text Preview': [text[:100] + "..." if len(text) > 100 else text 
                                           for text in texts_to_analyze[:5]]
                        })
                        st.dataframe(preview_df)
                        
                        if len(texts_to_analyze) > 5:
                            st.info(f"Showing first 5 of {len(texts_to_analyze)} texts")
                
                except Exception as e:
                    st.error(f"❌ Error processing file: {e}")
        
        elif input_method == "Enter Text Directly":
            text_input = st.text_area(
                "Enter text to analyze (one per line):",
                height=200,
                placeholder="Enter your text here...\nEach line will be analyzed separately."
            )
            
            if text_input:
                texts_to_analyze = [line.strip() for line in text_input.split('\n') if line.strip()]
                metadata = {'source': 'Direct input', 'total_texts': len(texts_to_analyze)}
                
                if texts_to_analyze:
                    st.success(f"✅ Ready to analyze {len(texts_to_analyze)} texts")
        
        elif input_method == "Use Sample Data" or st.session_state.get('sample_data'):
            sample_data = data_processor.create_sample_data()
            texts_to_analyze = sample_data['texts']
            metadata = sample_data['metadata']
            
            st.success(f"✅ Loaded {len(texts_to_analyze)} sample texts")
            
            # Show sample data
            st.subheader("📋 Sample Data Preview")
            sample_df = pd.DataFrame({'Sample Texts': texts_to_analyze})
            st.dataframe(sample_df)
        
        # Analysis button
        if texts_to_analyze:
            col1, col2 = st.columns([1, 3])
            
            with col1:
                analyze_button = st.button("🚀 Analyze Sentiment", type="primary")
            
            with col2:
                st.info(f"Ready to analyze {len(texts_to_analyze)} texts")
            
            if analyze_button:
                # Perform analysis
                with st.spinner("🤖 AI is analyzing your text..."):
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    start_time = time.time()
                    
                    if len(texts_to_analyze) == 1:
                        # Single text analysis
                        status_text.text("Analyzing text...")
                        results = [analyzer.analyze_single_text(texts_to_analyze[0])]
                        progress_bar.progress(1.0)
                    else:
                        # Batch analysis
                        status_text.text("Analyzing batch...")
                        results = analyzer.analyze_batch(texts_to_analyze)
                        progress_bar.progress(1.0)
                    
                    # Calculate summary statistics
                    summary_stats = analyzer.get_summary_stats(results)
                    
                    end_time = time.time()
                    analysis_time = round(end_time - start_time, 2)
                    
                    # Store results in session state
                    st.session_state.analysis_results = results
                    st.session_state.summary_stats = summary_stats
                    st.session_state.metadata = metadata
                    st.session_state.analysis_time = analysis_time
                    
                    status_text.empty()
                    progress_bar.empty()
                
                st.success(f"✅ Analysis complete! Processed {len(results)} texts in {analysis_time}s")
                st.balloons()
    
    with tab2:
        st.header("📊 Analysis Results Dashboard")
        
        if 'analysis_results' in st.session_state:
            results = st.session_state.analysis_results
            summary_stats = st.session_state.summary_stats
            
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Total Analyzed",
                    summary_stats['total_analyzed'],
                    help="Total number of texts analyzed"
                )
            
            with col2:
                st.metric(
                    "Positive",
                    f"{summary_stats['positive_percentage']}%",
                    f"{summary_stats['positive_count']} texts"
                )
            
            with col3:
                st.metric(
                    "Negative", 
                    f"{summary_stats['negative_percentage']}%",
                    f"{summary_stats['negative_count']} texts"
                )
            
            with col4:
                st.metric(
                    "Avg Confidence",
                    f"{summary_stats['average_confidence']}",
                    help="Average confidence score (0-1)"
                )
            
            # Charts section - PLOTLY CHARTS
            st.subheader("📈 Visual Analysis")
            
            chart_col1, chart_col2 = st.columns(2)
            
            with chart_col1:
                # Sentiment pie chart
                pie_chart = chart_gen.create_sentiment_pie_chart(
                    summary_stats['positive_count'],
                    summary_stats['negative_count'],
                    summary_stats['neutral_count']
                )
                if pie_chart:
                    st.plotly_chart(pie_chart, use_container_width=True)
            
            with chart_col2:
                # Sentiment bar chart
                bar_chart = chart_gen.create_sentiment_bar_chart(
                    summary_stats['positive_count'],
                    summary_stats['negative_count'],
                    summary_stats['neutral_count']
                )
                if bar_chart:
                    st.plotly_chart(bar_chart, use_container_width=True)
            
            # Additional charts
            chart_col3, chart_col4 = st.columns(2)
            
            with chart_col3:
                confidence_chart = chart_gen.create_confidence_chart(results)
                if confidence_chart:
                    st.plotly_chart(confidence_chart, use_container_width=True)
            
            with chart_col4:
                intensity_chart = chart_gen.create_intensity_chart(results)
                if intensity_chart:
                    st.plotly_chart(intensity_chart, use_container_width=True)
            
            # Detailed results table
            st.subheader("📋 Detailed Results")
            
            # Create DataFrame for display
            display_data = []
            for i, result in enumerate(results):
                display_data.append({
                    'ID': i + 1,
                    'Text Preview': result['original_text'][:50] + "..." if len(result['original_text']) > 50 else result['original_text'],
                    'Sentiment': result['sentiment'].title(),
                    'Confidence': f"{result['confidence']:.2f}",
                    'Intensity': result['intensity'],
                    'Top Emotions': ', '.join(result['emotions'][:3]),
                    'Key Phrases': ', '.join(result['key_phrases'][:3])
                })
            
            results_df = pd.DataFrame(display_data)
            
            # Add filters
            col1, col2 = st.columns(2)
            with col1:
                sentiment_filter = st.selectbox(
                    "Filter by sentiment:",
                    ["All", "Positive", "Negative", "Neutral"]
                )
            
            with col2:
                min_confidence = st.slider(
                    "Minimum confidence:",
                    0.0, 1.0, 0.0, 0.1
                )
            
            # Apply filters
            filtered_df = results_df.copy()
            if sentiment_filter != "All":
                filtered_df = filtered_df[filtered_df['Sentiment'] == sentiment_filter]
            
            if min_confidence > 0:
                filtered_df = filtered_df[filtered_df['Confidence'].astype(float) >= min_confidence]
            
            st.dataframe(filtered_df, use_container_width=True)
            
            # Top emotions and phrases
            if summary_stats.get('top_emotions'):
                st.subheader("🎭 Top Emotions Detected")
                emotions_col1, emotions_col2 = st.columns(2)
                
                with emotions_col1:
                    for emotion, count in summary_stats['top_emotions'][:5]:
                        percentage = (count / summary_stats['total_analyzed']) * 100
                        st.write(f"**{emotion.title()}**: {count} ({percentage:.1f}%)")
                
                with emotions_col2:
                    # Create emotion chart using Plotly
                    emotion_chart = chart_gen.create_emotion_chart(summary_stats)
                    if emotion_chart:
                        st.plotly_chart(emotion_chart, use_container_width=True)
        
        else:
            st.info("👆 Please analyze some text in the 'Input & Analysis' tab first!")
    
    with tab3:
        st.header("📁 Export & Reports")
        
        if 'analysis_results' in st.session_state:
            results = st.session_state.analysis_results
            summary_stats = st.session_state.summary_stats
            metadata = st.session_state.metadata
            
            # Export options
            st.subheader("💾 Export Results")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # CSV Export
                csv_data = data_processor.export_results_csv(results, summary_stats)
                st.download_button(
                    label="📄 Download CSV Report",
                    data=csv_data,
                    file_name=f"sentiment_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            
            with col2:
                # JSON Export
                json_data = data_processor.export_results_json(results, summary_stats)
                st.download_button(
                    label="📋 Download JSON Report",
                    data=json_data,
                    file_name=f"sentiment_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
            
            # Analysis summary report
            st.subheader("📊 Analysis Summary Report")
            
            report_text = f"""
# Sentiment Analysis Report
**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Analysis Time:** {st.session_state.get('analysis_time', 'N/A')} seconds

## Data Source
- **Source:** {metadata.get('source', 'Unknown')}
- **Total Texts Analyzed:** {summary_stats['total_analyzed']}

## Sentiment Distribution
- **Positive:** {summary_stats['positive_count']} ({summary_stats['positive_percentage']}%)
- **Negative:** {summary_stats['negative_count']} ({summary_stats['negative_percentage']}%)
- **Neutral:** {summary_stats['neutral_count']} ({summary_stats['neutral_percentage']}%)

## Quality Metrics
- **Average Confidence:** {summary_stats['average_confidence']} / 1.0
- **Average Intensity:** {summary_stats['average_intensity']} / 10

## Top Emotions Detected
"""
            
            for emotion, count in summary_stats.get('top_emotions', [])[:5]:
                percentage = (count / summary_stats['total_analyzed']) * 100
                report_text += f"- **{emotion.title()}:** {count} ({percentage:.1f}%)\n"
            
            st.markdown(report_text)
            
            # Download report
            st.download_button(
                label="📝 Download Summary Report",
                data=report_text,
                file_name=f"sentiment_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown"
            )
            
        else:
            st.info("👆 Please analyze some text first to generate reports!")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    🤖 **Powered by Google Gemini AI** | 📊 **Charts by Plotly** | 🚀 **Built with Streamlit**
    
    💡 **Tip**: For best results, ensure your text is clear and contains emotional content.
    """)

if __name__ == "__main__":
    main()
