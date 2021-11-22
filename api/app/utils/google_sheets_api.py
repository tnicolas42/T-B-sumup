import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
# https://developers.google.com/sheets/api/guides/authorizing
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

class VALUE_INPUT_OPTION:  # https://developers.google.com/sheets/api/reference/rest/v4/ValueInputOption
    RAW = 'RAW'  # The values the user has entered will not be parsed and will be stored as-is.
    USER_ENTERED = 'USER_ENTERED'  # The values will be parsed as if the user typed them into the UI.
    DEFAULT = USER_ENTERED  # The default value

class MAJOR_DIMENSION:  # https://developers.google.com/sheets/api/reference/rest/v4/Dimension
    ROWS = 'ROWS'  # Operates on the rows of a sheet.
    COLUMNS = 'COLUMNS'  # Operates on the columns of a sheet.
    DEFAULT = ROWS  # The default value

class VALUE_RENDER_OPTION:  # https://developers.google.com/sheets/api/reference/rest/v4/ValueRenderOption
    FORMATTED_VALUE = 'FORMATTED_VALUE'  # Values will be calculated & formatted in the reply according to the cell's formatting.
    UNFORMATTED_VALUE = 'UNFORMATTED_VALUE'  # Values will be calculated, but not formatted in the reply.
    FORMULA = 'FORMULA'  # Values will not be calculated.
    DEFAULT = FORMATTED_VALUE  # The default value

class DATE_TIME_RENDER_OPTION:  # https://developers.google.com/sheets/api/reference/rest/v4/DateTimeRenderOption
    SERIAL_NUMBER = 'SERIAL_NUMBER'
    FORMATTED_STRING = 'FORMATTED_STRING'
    DEFAULT = FORMATTED_STRING  # The default value

class GoogleSheetsApi:
    service = None  # google sheet api service

    def __init__(self):
        pass


    def connect_api(self):
        """
        Connect to the google sheet API.

        Parameters:
          
        Returns:
            GoogleSheetsApi: The self element.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        self.service = build('sheets', 'v4', credentials=creds)
        return self


    def batch_get_range(self,
        cells,
        file_id,
        sheet_name,
        major_dimension=MAJOR_DIMENSION.DEFAULT,
        value_render_option=VALUE_RENDER_OPTION.DEFAULT,
        date_time_render_option=DATE_TIME_RENDER_OPTION.DEFAULT):
        """
        Read values in multiples specified range.
        https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/get

        Parameters:
            cells (list[str]): The list of ranges (eg. ['A1:C12', 'E2']).
            file_id (str): The spreadseet id.
            sheet_name (str): The sheetname in the spreadsheet.
            major_dimension (str): The major dimension that results should use.
            value_render_option (str): How values should be represented in the output.
            date_time_render_option (str): How dates, times, and durations should be represented in the output.
          
        Returns:
            list: The readed values (eg. [ [ [ 12, 'ok' ], [ 3, 4 ] ] [[ 'test' ]] ]).
        """
        ranges = []
        for single_range in cells:
            ranges.append(sheet_name + '!' + single_range)
        print(ranges)
        sheet = self.service.spreadsheets()
        result = sheet.values().batchGet(spreadsheetId=file_id,
                                    ranges=ranges,
                                    majorDimension=major_dimension,
                                    valueRenderOption=value_render_option,
                                    dateTimeRenderOption=date_time_render_option,
                                    ).execute()
        # return a list of ValueRange https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values#ValueRange
        # print(result)
        # print(type(result))
        # values = result.get('values', [])
        values = []
        for res in result['valueRanges']:
            values.append(res['values'])
        return values


    def batch_get_cell(self,
        cells,
        file_id,
        sheet_name,
        major_dimension=MAJOR_DIMENSION.DEFAULT,
        value_render_option=VALUE_RENDER_OPTION.DEFAULT,
        date_time_render_option=DATE_TIME_RENDER_OPTION.DEFAULT):
        """
        Read values in multiples specified range.
        https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/get

        Parameters:
            cells (list[str]): The list of cells (eg. ['A1', 'E2']).
            file_id (str): The spreadseet id.
            sheet_name (str): The sheetname in the spreadsheet.
            major_dimension (str): The major dimension that results should use.
            value_render_option (str): How values should be represented in the output.
            date_time_render_option (str): How dates, times, and durations should be represented in the output.
          
        Returns:
            list: The readed values (eg. [ 12, 'ok' ]).
        """
        batch_result = self.batch_get_range(
            cells=cells,
            file_id=file_id,
            sheet_name=sheet_name,
            major_dimension=major_dimension,
            value_render_option=value_render_option,
            date_time_render_option=date_time_render_option)
        result = []
        for res in batch_result:
            result.append(res[0][0])
        return result
    

    def get_range(self,
        cells,
        file_id,
        sheet_name,
        major_dimension=MAJOR_DIMENSION.DEFAULT,
        value_render_option=VALUE_RENDER_OPTION.DEFAULT,
        date_time_render_option=DATE_TIME_RENDER_OPTION.DEFAULT):
        """
        Read values in a specified range.
        https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/get

        Parameters:
            cells (str): The range (eg. 'A1:C12').
            file_id (str): The spreadseet id.
            sheet_name (str): The sheetname in the spreadsheet.
            major_dimension (str): The major dimension that results should use.
            value_render_option (str): How values should be represented in the output.
            date_time_render_option (str): How dates, times, and durations should be represented in the output.
          
        Returns:
            list: The readed values (eg. [ [ 12, 'ok' ], [ 3, 4 ] ]).
        """
        sheet = self.service.spreadsheets()
        result = sheet.values().get(spreadsheetId=file_id,
                                    range=sheet_name + '!' + cells,
                                    majorDimension=major_dimension,
                                    valueRenderOption=value_render_option,
                                    dateTimeRenderOption=date_time_render_option,
                                    ).execute()
        # return a ValueRange https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values#ValueRange
        values = result.get('values', [])
        return values


    def get_cell(self, cell, file_id, sheet_name):
        """
        Read values in a specified range

        Parameters:
            cell (str): The cell (eg. 'A1').
            file_id (str): The spreadseet id.
            sheet_name (str): The sheetname in the spreadsheet.
          
        Returns:
            type: The readed value in the right type.
        """
        return self.get_range(file_id=file_id, sheet_name=sheet_name, cells=cell)[0][0]


    def batch_update_range(self, cells, values, file_id, sheet_name, value_input_option=VALUE_INPUT_OPTION.DEFAULT, major_dimension=MAJOR_DIMENSION.DEFAULT):
        """
        Write values in a specified range
        https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/batchUpdate

        Parameters:
            cells (list[str]): The range list (eg. 'A1:C12').
            values (list): The values to put in the range (eg. [ [ 12, 'ok' ], [ 3, 4 ] ]).
            file_id (str): The spreadseet id.
            sheet_name (str): The sheetname in the spreadsheet.
            value_input_option (str): Element in VALUE_INPUT_OPTION class.
          
        Returns:
            int: The number of cells updated.
        """
        body = {
            'value_input_option': value_input_option,
            'data': []
        }
        for idx, cell in enumerate(cells):
            body['data'].append({
                "range": sheet_name + '!' + cell,
                "majorDimension": major_dimension,
                "values": values[idx],
            })
        result = self.service.spreadsheets().values().batchUpdate(
            spreadsheetId=file_id,
            body=body).execute()
        return result.get('updatedCells')


    def batch_update_cell(self, cells, values, file_id, sheet_name, value_input_option=VALUE_INPUT_OPTION.DEFAULT, major_dimension=MAJOR_DIMENSION.DEFAULT):
        """
        Write values in a specified range
        https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/batchUpdate

        Parameters:
            cells (list[str]): The range list (eg. 'A1:C12').
            values (list): The values to put in the range (eg. [ [ 12, 'ok' ], [ 3, 4 ] ]).
            file_id (str): The spreadseet id.
            sheet_name (str): The sheetname in the spreadsheet.
            value_input_option (str): Element in VALUE_INPUT_OPTION class.
          
        Returns:
            int: The number of cells updated.
        """
        values_new = []
        for val in values:
            values_new.append([[val]])
        return self.batch_update_range(
            cells=cells,
            values=values_new,
            file_id=file_id,
            sheet_name=sheet_name,
            value_input_option=value_input_option,
            major_dimension=major_dimension,
        )


    def update_range(self, cells, values, file_id, sheet_name, value_input_option=VALUE_INPUT_OPTION.DEFAULT):
        """
        Write values in a specified range
        https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/update

        Parameters:
            cells (str): The range (eg. 'A1:C12').
            values (list): The values to put in the range (eg. [ [ 12, 'ok' ], [ 3, 4 ] ]).
            file_id (str): The spreadseet id.
            sheet_name (str): The sheetname in the spreadsheet.
            value_input_option (str): Element in VALUE_INPUT_OPTION class.
          
        Returns:
            int: The number of cells updated.
        """
        body = {
            'values': values
        }
        result = self.service.spreadsheets().values().update(
            spreadsheetId=file_id,
            range=sheet_name + '!' + cells,
            valueInputOption=value_input_option,
            body=body).execute()
        return result.get('updatedCells')


    def update_value(self, cell, value, file_id, sheet_name, value_input_option=VALUE_INPUT_OPTION.DEFAULT):
        """
        Write value in a specified cell

        Parameters:
            cells (str): The range (eg. 'A1:C12').
            values (list): The values to put in the range (eg. [ [ 12, 'ok' ], [ 3, 4 ] ]).
            file_id (str): The spreadseet id.
            sheet_name (str): The sheetname in the spreadsheet.
            value_input_option (str): Element in VALUE_INPUT_OPTION class.
          
        Returns:
            int: The number of cells updated.
        """
        return self.write_range(file_id=file_id, sheet_name=sheet_name, cells=cell, values=[[value]], value_input_option=value_input_option)


if __name__ == '__main__':
    gsheet = GoogleSheetsApi().connect_api()

    file_info = dict(
        file_id='17BxVhEaZ8KN_nrV2ZM1TgkdT4fpjea2eyS5HRi-yyqA',
        sheet_name='Sheet1',
    )

    values = gsheet.get_range(cells='A1:B3', **file_info)
    print(values)

    print(gsheet.get_cell(cell='A2', **file_info))

    gsheet.update_range(cells='A2:B2', values=[[12, 14]], **file_info)

    gsheet.update_value(cell='C1', value='=12+3', **file_info)