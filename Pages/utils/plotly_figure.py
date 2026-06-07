import plotly.graph_objects as go
import dateutil
import pandas_ta_classic as pta
import datetime

import plotly.graph_objects as go

def plotly_table(dataframe):
    headerColor = '#0078ff' # Changed to match your fillcolor choice
    roundEvenColor = '#f8fafd'
    roundOddColor = '#e1efff' # Fixed invalid hex code ('l' to '1')
    
    fig = go.Figure(go.Table( # Fixed .figure[ to .Figure(
        header=dict(
            # Fixed the bold tag and extracted clean column names
            values = ['<b></b>'] + ['<b>'+str(i)[:10]+'</b>' for i in dataframe.columns],
            line_color='#0078ff', # Fixed linecolor to line_color
            fill_color='#0078ff', # Fixed fillcolor to fill_color
            align='center',       # Fixed 'centre' to 'center'
            font=dict(color='white', size=15),
            height=35
        ),
        cells=dict(
            # Fixed the list concatenation logic for index and columns
            values = [['<br>'+str(idx)+'<br>' for idx in dataframe.index]] + [dataframe[col] for col in dataframe.columns],
            fill_color=[[roundOddColor if i % 2 == 0 else roundEvenColor for i in range(len(dataframe))]], 
            line_color='white',   # Fixed linecolor to line_color
            align='left',
            font=dict(color='black', size=15)
        )
    ))
    
    # Fixed the margin dictionary syntax (colon instead of equals)
    fig.update_layout(height=400, margin=dict(l=0, r=0, t=0, b=0))
    return fig

def filter_data(dataframe,num_period):
    if num_period =='5d':
        date = dataframe.index[-1]+dateutil.relativedelta.relativedelta(days=-5)
    
    elif num_period =='1mo':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(months=-1)

    elif num_period =='6mo':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(months=-6)

    elif num_period =='1y':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(years=-1)

    elif num_period =='5y':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(years=-5)

    elif num_period =='ytd':
        date = datetime.datetime(dataframe.index[-1].year,1,1).strftime('%Y-%m-%d')

    else:
        date = dataframe.index[0]

    return dataframe.reset_index()[dataframe.reset_index()['Date']>date]

def close_chart(dataframe , num_peroid = False):
    if num_peroid:
        dataframe = filter_data(dataframe,num_peroid)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x = dataframe['Date'],y=dataframe['Open'],mode = 'lines',name ='Open',line = dict(width = 2,color ='#5ab7ff')))

    fig.add_trace(go.Scatter(x = dataframe['Date'],y=dataframe['Close'],mode = 'lines',name ='Close',line = dict(width = 2,color ='black')))

    fig.add_trace(go.Scatter(x = dataframe['Date'],y=dataframe['High'],mode = 'lines',name ='High',line = dict(width = 2,color ='#0078ff')))

    fig.add_trace(go.Scatter(x = dataframe['Date'],y=dataframe['Low'],mode = 'lines',name ='Low',line = dict(width = 2,color ='red')))

    fig.update_xaxes(rangeslider_visible = True)

    fig.update_layout(height=500,margin=dict(l=50, r=20, t=20, b=50),plot_bgcolor = 'white',paper_bgcolor = '#e1efff',legend =dict(
        yanchor = 'top',
        xanchor = 'left'
    ))

    return fig

def candlestick(dataframe,num_peroid):
    dataframe = filter_data(dataframe,num_peroid)
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x = dataframe['Date'],open=dataframe['Open'],high = dataframe['High'],low=dataframe['Low'],close = dataframe['Close']))
    fig.update_layout(height=500,margin=dict(l=50, r=20, t=20, b=50),plot_bgcolor = 'white',paper_bgcolor = '#e1efff',showlegend = False)

    return fig


def RSI(dataframe,num_peroid):
    dataframe['RSI'] = pta.rsi(dataframe['Close'])
    dataframe = filter_data(dataframe,num_peroid)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x  = dataframe['Date'] , y= dataframe.RSI,name = 'RSI',marker_color ='orange',line = dict(width=2,color='orange')
    ))

    fig.add_trace(go.Scatter(
        x  = dataframe['Date'] , y= [70]*len(dataframe),name = 'Overbought',marker_color ='orange',line = dict(width=2,color='red',dash ='dash')
    ))

    fig.add_trace(go.Scatter(
        x  = dataframe['Date'] , y= [30]*len(dataframe),name = 'Oversold',marker_color ='orange',line = dict(width=2,color='green',dash ='dash')
    ))

    fig.update_layout(yaxis_range =[0,100],height=500,margin=dict(l=50, r=20, t=20, b=50),plot_bgcolor = 'white',paper_bgcolor = '#e1efff',legend =dict(
        orientation = 'h',
        y=1.02,
        x=1,
        yanchor = 'bottom',
        xanchor = 'right'
    ))

    return fig

def moving_average(dataframe , num_peroid ):
   
    dataframe['SMA_50'] = pta.sma(dataframe['Close'],50)
    dataframe = filter_data(dataframe,num_peroid)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x = dataframe['Date'],y=dataframe['Open'],mode = 'lines',name ='Open',line = dict(width = 2,color ='#5ab7ff')))

    fig.add_trace(go.Scatter(x = dataframe['Date'],y=dataframe['Close'],mode = 'lines',name ='Close',line = dict(width = 2,color ='black')))

    fig.add_trace(go.Scatter(x = dataframe['Date'],y=dataframe['High'],mode = 'lines',name ='High',line = dict(width = 2,color ='#0078ff')))

    fig.add_trace(go.Scatter(x = dataframe['Date'],y=dataframe['Low'],mode = 'lines',name ='Low',line = dict(width = 2,color ='red')))

    fig.add_trace(go.Scatter(x = dataframe['Date'],y=dataframe['SMA_50'],mode = 'lines',name ='SMA_50',line = dict(width = 2,color ='purple')))


    fig.update_xaxes(rangeslider_visible = True)

    fig.update_layout(height=500,margin=dict(l=50, r=20, t=20, b=50),plot_bgcolor = 'white',paper_bgcolor = '#e1efff',legend =dict(
        yanchor = 'top',
        xanchor = 'right'
    ))

    return fig


def MACD(dataframe,num_peroid):
    macd= pta.macd(dataframe['Close'])
 
    dataframe['MACD'] = macd.iloc[:, 0]
    dataframe['MACD Hist'] = macd.iloc[:, 1]
    dataframe['MACD Signal'] = macd.iloc[:, 2]

    macd_hist = pta.macd(dataframe['Close']).iloc[:,2]


    dataframe = filter_data(dataframe,num_peroid)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x  = dataframe['Date'] , y= dataframe['MACD'],name = 'MACD',marker_color ='orange',line = dict(width=2,color='orange')
    ))

    fig.add_trace(go.Scatter(
        x  = dataframe['Date'] , y= dataframe['MACD Signal'],name = 'MACD Signal',marker_color ='orange',line = dict(width=2,color='red',dash = 'dash')
    ))

    c=['red' if cl<0 else 'green' for cl in macd_hist]

    fig.add_trace(go.Bar(
    x=dataframe['Date'], 
    y=dataframe['MACD Hist'], 
    name='Histogram',
    marker_color=c
    ))

    fig.update_layout(yaxis_range =[0,100],height=500,margin=dict(l=50, r=20, t=20, b=50),plot_bgcolor = 'white',paper_bgcolor = '#e1efff',legend =dict(
        orientation = 'h',
        y=1.02,
        x=1,
        yanchor = 'top',
        xanchor = 'right'
    ))

    return fig

def moving_average_forecast(forecast,days):
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=forecast.index[:-days],y=forecast['close'].iloc[:-days],mode = 'lines',name ='Close_Price',line = dict(width = 2,color ='black')))
    fig.add_trace(go.Scatter(x=forecast.index[-days-1:],y=forecast['close'].iloc[-days-1:],mode = 'lines',name ='Future_Close_Price',line = dict(width = 2,color ='red')))

    fig.update_xaxes(rangeslider_visible = True)

    fig.update_layout(height=500,margin=dict(l=50, r=20, t=20, b=50),plot_bgcolor = 'white',paper_bgcolor = '#e1efff',legend =dict(
        yanchor = 'top',
        xanchor = 'left'
    ))

    return fig




def plotly_tab(dataframe):
    headerColor = '#0078ff' 
    roundEvenColor = '#f8fafd'
    roundOddColor = '#e1efff' 
    
    # --- 1. DYNAMIC HEIGHT CALCULATOR ---
    header_height = 35
    row_height = 40  # Slightly increased row height for clear spacing
    
    # Calculate exactly how much vertical space the table contents need
    content_height = header_height + (len(dataframe) * row_height)
    
    # Add a safety margin below the table so the next step has breathing room
    bottom_gap = 40 
    total_calculated_height = content_height + bottom_gap
    
    # Set boundaries: don't let it shrink to nothing, and don't let it become infinitely long
    final_height = max(120, min(total_calculated_height, 600))
    
    # --- 2. CREATE THE TABLE ---
    fig = go.Figure(go.Table(
        header=dict(
            values = ['<b>Index</b>'] + [f'<b>{str(col)}</b>' for col in dataframe.columns],
            line_color=headerColor,
            fill_color=headerColor,
            align='center',       
            font=dict(color='white', size=15),
            height=header_height
        ),
        cells=dict(
            values = [dataframe.index.astype(str)] + [dataframe[col] for col in dataframe.columns],
            # Pattern matching alternating row colors perfectly
            fill_color=[[roundEvenColor if i % 2 == 0 else roundOddColor for i in range(len(dataframe))]], 
            line_color='#e1efff',   
            align='center',  # Switched to center for a cleaner financial dashboard vibe
            font=dict(color='#1e293b', size=14), # Soft dark gray text for readability
            height=row_height
        )
    ))
    
    # --- 3. APPLY DYNAMIC LAYOUT & REMOVE MARGIN WASTAGE ---
    fig.update_layout(
        height=final_height,
        margin=dict(l=0, r=0, t=10, b=10), # Strips out useless outer borders
        autosize=True
    )
    
    return fig


def dynamic_plotly_table(dataframe):
    # --- 1. Color Theme ---
    header_color = '#0078ff' 
    row_even_color = '#f8fafd'
    row_odd_color = '#e1efff' 
    text_color = '#1e293b' # Soft dark slate for better readability than pure black
    
    # --- 2. Dynamic Height Calculation ---
    header_height = 40
    row_height = 35
    
    # Calculate exactly how much vertical space the table contents need
    # (Header + (Number of rows * Height per row) + tiny buffer for borders)
    calculated_height = header_height + (len(dataframe) * row_height) + 20
    
    # Set a maximum height (e.g., 800px) just in case you ever pass 100 rows, 
    # so it doesn't take over the entire webpage.
    final_height = min(max(calculated_height, 100), 800) 
    
    # --- 3. Create the Table ---
    fig = go.Figure(go.Table(
        header=dict(
            values = ['<b>Index</b>'] + [f'<b>{str(col)}</b>' for col in dataframe.columns],
            line_color=header_color,
            fill_color=header_color,
            align='center',       
            font=dict(color='white', size=15),
            height=header_height
        ),
        cells=dict(
            values = [dataframe.index.astype(str)] + [dataframe[col] for col in dataframe.columns],
            fill_color=[[row_odd_color if i % 2 == 0 else row_even_color for i in range(len(dataframe))]], 
            line_color='white',   
            align='center',  # Centered numbers usually look cleaner for data dashboards
            font=dict(color=text_color, size=14),
            height=row_height
        )
    ))
    
    # --- 4. Apply Dynamic Layout & Remove Wasted Space ---
    fig.update_layout(
        height=final_height,
        margin=dict(l=0, r=0, t=10, b=10), # Crucial: strips out Plotly's default massive borders
        autosize=True
    )
    
    return fig