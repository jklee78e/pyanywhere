import os
from flask import Flask, render_template, request, jsonify
from pandas_datareader import data as pdr
import numpy as np


app = Flask(__name__)

# FRED API 키 설정
FRED_API_KEY = 'c48f5f120f822ecf8187d20c7319ed1f'
os.environ["FRED_API_KEY"] = FRED_API_KEY

# 가장 인기 있는 데이터 시리즈 코드 목록
popular_series = [
    "GDP", "CPIAUCSL", "UNRATE", "DGS10", "SP500", "FEDFUNDS",
    # 추가 데이터 시리즈 코드
]

@app.route('/')
def index():
    return render_template('index.html', series=popular_series)

@app.route('/data', methods=['POST'])
def get_data():
    selected_series = request.form.getlist('series')
    data_frames = {}
    descriptions = {}
    units = {}

    for series in selected_series:
        description = request.form.get(f'description_{series}', '')
        unit = request.form.get(f'unit_{series}', '')
        
        try:
            df = pdr.get_data_fred(series)
            data_frames[series] = df
            descriptions[series] = description
            units[series] = unit
        except Exception as e:
            data_frames[series] = f"Error: {e}"
    
    return render_template('data.html', data_frames=data_frames, descriptions=descriptions, units=units)


@app.route('/fetch_chart_data')
def fetch_chart_data():
    series = request.args.get('series')
    try:
        df = pdr.get_data_fred(series)
        if df.empty:
            return jsonify({"error": "No data returned from FRED API."})
        
        df = df.reset_index()  # Ensure 'DATE' is in the dataframe
        if 'DATE' not in df.columns:
            return jsonify({"error": "DATE column is missing from the data."})
        
        df.rename(columns={'DATE': 'date', series: 'value'}, inplace=True)
        df['date'] = df['date'].dt.strftime('%Y-%m-%d')
        
        # Convert NaN to None
        df['value'] = df['value'].replace({np.nan: None})
        
        return jsonify(df[['date', 'value']].to_dict(orient='records'))
    except Exception as e:
        return jsonify({"error": str(e)})



if __name__ == '__main__':
    app.run(debug=True)
