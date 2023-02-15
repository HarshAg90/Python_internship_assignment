from alpha_vantage.timeseries import TimeSeries
import pandas
import copy

#Y455ZZ06T6P3LRSW
#Y455ZZ06T6P3LRSW
#Y455ZZ06T6P3LRSW

class ScriptData:
    def __init__(self):
        self.key = TimeSeries(key="Y455ZZ06T6P3LRSW", output_format = 'pandas', indexing_type='integer')
        self.df = {}
        pass

    def __getitem__(self,script):
        if script in self.df:
            return self.df[script]
        else:
            return "not found"

    def fetch_intraday_data(self,script):
        self.df[script], mata_data = self.key.get_intraday(script)
        pass
    def convert_intray_data(self,script):
        self.df[script].rename(columns={"index":"timestamp", "1. open": "open","2. high":"high","3. low":"low","4. close":"close","5. volume":"volume"}, inplace=True)
        pass


def indicator1(df,timeperiod:int):
    df.drop(columns=["open","high","low","volume"],inplace=True)
    df.rename(columns={"close":"indicator"},inplace=True)
    df_new = copy.copy(df)

    for i in range(0,len(df["timestamp"])):
        if i<= timeperiod:
            df_new.at[i,"indicator"] = "NAN"
        else:
            try:
                df_new.at[i,"indicator"] = sum(df["indicator"].iloc[i-timeperiod : i+1])/timeperiod
            except:
                print(i,type(i))
    return df_new

# obj = ScriptData()
# obj.fetch_intraday_data("GOOGL")
# obj.convert_intray_data("GOOGL")
# print(obj["GOOGL"][:15])
# print(indicator1(obj['GOOGL'],5)[:15])

class Strategy:
    def __init__(self,script):
        self.id = script
        self.data = None
        self.predictor = None
        self.signal = None
        self.timeperiod= 5
    def get_script_data(self):
        data_obj = ScriptData()
        data_obj.fetch_intraday_data(self.id)
        data_obj.convert_intray_data(self.id)
        self.data = data_obj[self.id]
        self.predictor = indicator1(copy.copy(self.data),self.timeperiod)

        self.signal = copy.copy(self.predictor)
        self.signal.rename(columns={"indicator":"signal"},inplace=True)

        for i in range(self.timeperiod+1,len( self.signal["timestamp"])):
            # try:
                if self.data["close"].iloc[i+1] < self.predictor["indicator"].iloc[i] and self.data["close"].iloc[i-1] > self.predictor["indicator"].iloc[i] and self.data["close"].iloc[i] == self.predictor["indicator"].iloc[i]:
                    self.signal.at[i,"signal"] = "BUY"
                elif self.data["close"].iloc[i+1] > self.predictor["indicator"].iloc[i] and self.data["close"].iloc[i-1] < self.predictor["indicator"].iloc[i] and self.data["close"].iloc[i] == self.predictor["indicator"].iloc[i]:
                    self.signal.at[i,"signal"] = "SELL"
                elif self.data["close"].iloc[i] != self.predictor["indicator"].iloc[i]:
                    self.signal.at[i,"signal"] = "NO_SIGNAL"
                else:
                    print("did not work")      
            # except:
            #     print(i)
    def get_signals(self):
        return self.signal
strategy = Strategy("GOOGL")
strategy.get_script_data()
print(strategy.get_signals()[90:120])