import logging
from io import BytesIO

import pandas as pd

logger = logging.getLogger(__name__)

def makeexcel(data: list) -> bytes:
    dfs = {}
    if len(data) == 0:
        raise Exception('empty data')
    union_data = data.pop().get('results', [])
    for item in data:
        union_data = union_data + item.get('results', [])
    try:
        for result in union_data:
            data_by_columns = {}
            for record in result["data"]:
                for k, v in record.items():
                    if k not in data_by_columns.keys():
                        data_by_columns[k] = [v]
                    else:
                        data_by_columns[k].append(v)
            df = pd.DataFrame.from_dict(data_by_columns, orient='index')
            df.transpose()
            dfs[result["index_name"]] = df
    except Exception as e:
        logger.error('error adding %s : %s ' % (result["index_name"], str(e)))

    buf = BytesIO()
    writer = pd.ExcelWriter(buf, engine='xlsxwriter')
    for sheet_name, df in dfs.items():
        df.to_excel(writer, sheet_name=sheet_name[:30])     # sheet_name must be less than 30 symbols
    writer.save()
    res = buf.getvalue()
    buf.close()
    return res
