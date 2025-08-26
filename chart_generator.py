import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class ChartGenerator:
    def __init__(self):
        # Plotly doesn't need initialization
        self.colors = {
            'positive': '#4CAF50',
            'negative': '#F44336', 
            'neutral': '#FFC107'
        }
    
    def create_sentiment_pie_chart(self, positive, negative, neutral):
        """Create interactive pie chart with Plotly"""
        if positive + negative + neutral == 0:
            return None
        
        labels = ['Positive', 'Negative', 'Neutral']
        values = [positive, negative, neutral]
        colors = [self.colors['positive'], self.colors['negative'], self.colors['neutral']]
        
        fig = px.pie(
            values=values, 
            names=labels,
            title="Sentiment Distribution",
            color_discrete_sequence=colors,
            width=400,
            height=300
        )
        
        # Customize appearance
        fig.update_traces(
            textposition='inside', 
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
        )
        
        fig.update_layout(
            showlegend=True,
            font=dict(size=12),
            margin=dict(t=50, b=20, l=20, r=20)
        )
        
        return fig
    
    def create_sentiment_bar_chart(self, positive, negative, neutral):
        """Create interactive bar chart with Plotly"""
        if positive + negative + neutral == 0:
            return None
        
        labels = ['Positive', 'Negative', 'Neutral']
        values = [positive, negative, neutral]
        colors = [self.colors['positive'], self.colors['negative'], self.colors['neutral']]
        
        fig = px.bar(
            x=labels,
            y=values,
            title="Sentiment Comparison",
            color=labels,
            color_discrete_sequence=colors,
            width=400,
            height=300
        )
        
        # Customize appearance
        fig.update_traces(
            hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
        )
        
        fig.update_layout(
            showlegend=False,
            xaxis_title="Sentiment",
            yaxis_title="Count",
            font=dict(size=12),
            margin=dict(t=50, b=50, l=50, r=20)
        )
        
        return fig
    
    def create_confidence_chart(self, results):
        """Create confidence distribution chart"""
        if not results:
            return None
        
        # Group by confidence ranges
        high = sum(1 for r in results if r.get('confidence', 0) >= 0.8)
        medium = sum(1 for r in results if 0.5 <= r.get('confidence', 0) < 0.8)
        low = sum(1 for r in results if r.get('confidence', 0) < 0.5)
        
        if high + medium + low == 0:
            return None
        
        labels = ['High (0.8-1.0)', 'Medium (0.5-0.8)', 'Low (0.0-0.5)']
        values = [high, medium, low]
        colors = ['#2E7D32', '#FFA000', '#D32F2F']
        
        fig = px.pie(
            values=values,
            names=labels,
            title="Confidence Distribution",
            color_discrete_sequence=colors,
            width=400,
            height=300
        )
        
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
        )
        
        fig.update_layout(
            showlegend=True,
            font=dict(size=12),
            margin=dict(t=50, b=20, l=20, r=20)
        )
        
        return fig
    
    def create_intensity_chart(self, results):
        """Create intensity distribution chart"""
        if not results:
            return None
        
        # Group by intensity ranges
        low = sum(1 for r in results if r.get('intensity', 5) <= 3)
        medium = sum(1 for r in results if 4 <= r.get('intensity', 5) <= 6)
        high = sum(1 for r in results if r.get('intensity', 5) >= 7)
        
        if low + medium + high == 0:
            return None
        
        labels = ['Low (1-3)', 'Medium (4-6)', 'High (7-10)']
        values = [low, medium, high]
        colors = ['#81C784', '#FFB74D', '#E57373']
        
        fig = px.bar(
            x=labels,
            y=values,
            title="Intensity Distribution",
            color=labels,
            color_discrete_sequence=colors,
            width=400,
            height=300
        )
        
        fig.update_traces(
            hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
        )
        
        fig.update_layout(
            showlegend=False,
            xaxis_title="Intensity Level",
            yaxis_title="Count",
            font=dict(size=12),
            margin=dict(t=50, b=50, l=50, r=20)
        )
        
        return fig
    
    def create_emotion_chart(self, summary_stats):
        """Create emotion frequency chart"""
        if not summary_stats.get('top_emotions'):
            return None
        
        emotions = [e[0] for e in summary_stats['top_emotions'][:5]]
        counts = [e[1] for e in summary_stats['top_emotions'][:5]]
        
        fig = px.bar(
            x=counts,
            y=emotions,
            orientation='h',
            title="Top Emotions Detected",
            color=counts,
            color_continuous_scale='Viridis',
            width=400,
            height=300
        )
        
        fig.update_traces(
            hovertemplate='<b>%{y}</b><br>Count: %{x}<extra></extra>'
        )
        
        fig.update_layout(
            showlegend=False,
            xaxis_title="Frequency",
            yaxis_title="Emotions",
            font=dict(size=12),
            margin=dict(t=50, b=50, l=100, r=20),
            coloraxis_showscale=False
        )
        
        return fig
