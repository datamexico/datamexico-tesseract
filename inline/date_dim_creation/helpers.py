def data_from_table(db_connector, table_name, date_dim):
    query = 'SELECT MIN({}), MAX({}) from {} WHERE {} > 1;'.format(date_dim, date_dim, table_name, date_dim)
    result = db_connector.raw_query(query)[0]
    data = {
        'level': date_dim,
        'len': len(str(result[0])),
        'max': result[1],
        'min': result[0]
    }
    return data

def inline_table(df, cube_name, data):
    depth = data['level']
    if depth == 'year':
        print('<InlineTable alias="dim_inline_{}">'.format(cube_name))
        for item in df.itertuples():
            print('\t<Row>')
            print('\t\t<Value column="id">{}</Value>'.format(item.year))
            print('\t\t<Value column="year">{}</Value>'.format(item.year))
            print('\t</Row>')

        print('</InlineTable>')
    elif depth == 'quarter_id':
        print('<InlineTable alias="dim_inline_{}">'.format(cube_name))
        for item in df.itertuples():
            print('\t<Row>')
            print('\t\t<Value column="id">{}</Value>'.format(item.quarter_id))
            print('\t\t<Value column="quarter">{}</Value>'.format(item.quarter))
            print('\t\t<Value column="year">{}</Value>'.format(item.year))
            print('\t</Row>')

        print('</InlineTable>')
    elif depth == 'month_id':
        print('<InlineTable alias="dim_inline_{}">'.format(cube_name))
        for item in df.itertuples():
            print('\t<Row>')
            print('\t\t<Value column="id">{}</Value>'.format(item.month_id))
            print('\t\t<Value column="month">{}</Value>'.format(item.month))
            print('\t\t<Value column="quarter">{}</Value>'.format(item.quarter))
            print('\t\t<Value column="year">{}</Value>'.format(item.year))
            print('\t</Row>')

        print('</InlineTable>')
    else:
        print('bad arguments')

def create_dimension(data):
    import pandas as pd
    depth = data['level']
    if depth == 'year':
        start = '{}-01-01'.format(data['min'])
        end = '{}-12-31'.format(data['max'])
        df = pd.DataFrame({"date": pd.date_range(start, end)})
        df['year'] = df.date.dt.year
        df.drop_duplicates(subset=depth, inplace=True)
        print(df.columns)
        return df
    elif depth == 'quarter_id':
        start = '{}-01-01'.format(str(data['min'])[:4])
        end = '{}-12-31'.format(str(data['max'])[:4])
        df = pd.DataFrame({"date": pd.date_range(start, end)})
        df["quarter"] = df.date.dt.year.astype(str) + "-Q" + df.date.dt.quarter.astype(str)
        df["quarter_id"] = (df.date.dt.year.astype(str) + df.date.dt.quarter.astype(str)).astype(int)
        df["year"] = df.date.dt.year
        df.drop_duplicates(subset=depth, inplace=True)
        df.drop(columns='date', inplace=True)
        print(df.columns)
        return df
    elif depth == 'month_id':
        start = '{}-{}-01'.format(str(data['min'])[:4], str(data['min'])[5:7])
        end = '{}-{}-31'.format(str(data['max'])[:4], str(data['max'])[5:7])
        df = pd.DataFrame({"date": pd.date_range(start, end)})
        df["month"] = df.date.dt.year.astype(str) + "-" + df.date.dt.month.astype(str).str.zfill(2)
        df["month_id"] = (df.date.dt.year.astype(str) + df.date.dt.month.astype(str).str.zfill(2)).astype(int)
        df["quarter"] = df.date.dt.year.astype(str) + "-Q" + df.date.dt.quarter.astype(str)
        df["year"] = df.date.dt.year
        df.drop_duplicates(subset=depth, inplace=True)
        df.drop(columns='date', inplace=True)
        print(df.columns)
        return df
    elif depth == 'date_id':
        # TODO
        print('initializing parameters..')
        value = 'too many values...'
        return value