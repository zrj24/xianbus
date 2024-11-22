import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import pandas as pd
from datetime import datetime, timedelta
import os

font = FontProperties(fname="C:/Windows/Fonts/simhei.ttf", size=14)
def readData():
    DATA_PATH = 'E:/real/data'
    filelist = os.listdir(DATA_PATH)
    filelist = [s for s in filelist if s.endswith('.csv') and len(s[:-4].rsplit('.', 1)[-1]) == 6 and s[:-4].rsplit('.', 1)[-1].isdigit()]
    filelist.sort()
    dfall = pd.DataFrame()
    for file in filelist:
        datestr = file[:-4]
        df = pd.read_csv(f'{DATA_PATH}/{file}', header=None)
        df['date'] = datestr
        dfall = pd.concat([dfall, df], ignore_index=True)
        
    dfall.columns=["bus", "line", 'date']
    dfall["d_numeric"], unique_d = pd.factorize(dfall["date"], sort=True)
    return dfall, unique_d

def plotLine(lineName = None, df = None, unique_d = None):
    if df is None:
        df, unique_d = readData()
    assert df is not None, "df is None"
    
    df_line = df[df['line'] == lineName]
    df_line = df_line.drop(['line'], axis=1)
    df_line["a_numeric"], unique_a = pd.factorize(df_line["bus"], sort=True)
    
    mpl.rcParams['figure.figsize'] = (max(3,len(unique_a)/6), max(6,len(unique_d)/6))
    plt.scatter(df_line["a_numeric"], df_line["d_numeric"])
    
    plt.xticks(range(len(unique_a)), unique_a, rotation=90)
    plt.yticks(range(len(unique_d)), unique_d)
    font = FontProperties(fname="C:/Windows/Fonts/simhei.ttf", size=14)
    plt.title(f"{lineName}", fontproperties=font)
    
    plt.tight_layout()


def analyzeLine(lineName = None):
    SRC_PATH = 'E:/real/src'
    PLOT_PATH = 'E:/xianbus/line/'
    df, unique_d = readData()
    if lineName is None:
        linecode = pd.read_csv(f'{SRC_PATH}/lineCodes.csv', header=None)
        lineNameList = linecode[0].to_list()
        # lineNameList = ['521路','229路','280路','215路','108路','266路','22路','36路','600路','616路']
        for lineName in lineNameList:
            plotLine(lineName, df, unique_d)
            plt.savefig(f'{PLOT_PATH}/{lineName}.png')
            print(f'saved {lineName}')
            plt.close()
    else:
        plotLine(lineName, df, unique_d)
        plt.show()

def plotBus(bus=None, df=None, unique_d=None):
    if df is None:
        df, unique_d = readData()
    assert df is not None, "df is None"
    df_bus = df[df['bus'] == bus]
    df_bus = df_bus.drop(['bus'], axis=1)

    df_bus["a_numeric"], unique_a = pd.factorize(df_bus["line"], sort=True)
    if len(unique_a) == 0:
        print(f'bus {bus} not found')
        return
    mpl.rcParams['figure.figsize'] = (max(3,len(unique_a)/6), max(6,len(unique_d)/6))
    plt.scatter(df_bus["a_numeric"], df_bus["d_numeric"])
    
    plt.xticks(range(len(unique_a)), unique_a, fontproperties=font)
    plt.yticks(range(len(unique_d)), unique_d)
    
    plt.title(f"{bus}", fontproperties=font)
    plt.tight_layout()

def analyzeBus(bus = None):
    PLOT_PATH = 'E:/real/plot/bus'
    if bus is None:
        df, unique_d = readData()
        buslist = list(df['bus'].unique())
        buslist = ['08-186002']
        for bus in buslist:
            # if df[df['bus'] == bus]['line'].unique().shape[0]>=2:
            # if df[df['bus'] == bus].shape[0]<3:
                plotBus(bus, df, unique_d)
                plt.savefig(f"{PLOT_PATH}/{bus}.png")
                print(f'saved {bus}')
                plt.close()
    else:
        plotBus(bus)
        plt.show()

def analyze_change_bus():
    from datetime import datetime
    DATA_PATH = 'E:/real/data'
    datestr = datetime.now().strftime('%y%m%d')
    # df = readData()
    df = None
    # buslist = list(df['bus'].unique())
    busdf = pd.read_csv(f'{DATA_PATH}/{datestr}_changeNew.csv', header=None)
    print(busdf)
    buslist = busdf[0].to_list()
    for bus in buslist:
        plotBus(bus, df)
        plt.show()
        plt.close()

def readDayData(datestr):
    datapath = 'E:/real/data/'
    filelist = os.listdir(datapath)
    if datestr is None:
        datestr = datetime.now().strftime('%y%m%d')
    filelist_thisday = [s for s in filelist if s.endswith('_.csv') and s.startswith(datestr)]
    filelist_thisday.sort()
    dfall = pd.DataFrame()
    for file in filelist_thisday:
        timestr = file[7:11]
        if timestr < '0300': continue
        df = pd.read_csv(datapath+file, header=None)
        if df.shape[1] == 5:
            df['anchor'] = 0
        df['time'] = int(timestr[:2])+int(timestr[2:])/60.0
        dfall = pd.concat([dfall, df], ignore_index=True)
    def nextdatestr(datestr):
        yy = int(datestr[:2])
        mm = int(datestr[2:4])
        dd = int(datestr[4:])
        dt = datetime(yy+2000, mm, dd)
        next_dt = dt + timedelta(days=1)
        nextDate = next_dt.strftime('%y%m%d')
        return nextDate
    filelist_nextday = [s for s in filelist if s.endswith('_.csv') and s.startswith(nextdatestr(datestr))]
    filelist_nextday.sort()
    for file in filelist_nextday:
        timestr = file[7:11]
        if timestr >= '0300': continue
        df = pd.read_csv(datapath+file, header=None)
        if df.shape[1] == 5:
            df['anchor'] = 0
        df['time'] = int(timestr[:2])+int(timestr[2:])/60.0+24.0
        dfall = pd.concat([dfall, df], ignore_index=True)
    dfall.columns=['line', 'linecode', 'direction', 'bus', 'section', 'anchor', 'time']
    dfall['bus'] = dfall['bus']
    return dfall

def plotDayLine(lineName = None, df = None, datestr=None):
    if df is None:
        df = readDayData(datestr)
    assert df is not None, "df is None"
    df_line = df[df['line'] == lineName]
    max_anchor_1 = df_line[df_line['direction']==1]['anchor'].max()
    max_anchor_2 = df_line[df_line['direction']==2]['anchor'].max()
    buses, unique_a = pd.factorize(df_line['bus'], sort=True)
    times = df_line['time']
    size = 17
    alpha = 0.8
    buses_1 = buses[(df_line['direction']==1) & (df_line['section']==0)]
    times_1 = times[(df_line['direction']==1) & (df_line['section']==0)]
    plt.scatter(buses_1, times_1, marker='o', c='#1f77b4', s=size, alpha=alpha)
    buses_2 = buses[(df_line['direction']==2) & (df_line['section']==0)]
    times_2 = times[(df_line['direction']==2) & (df_line['section']==0)]
    plt.scatter(buses_2, times_2, marker='o', c='#ff7f0e', s=size, alpha=alpha)
    buses_s_1 = buses[(df_line['direction']==1) & (df_line['section']==1)]
    times_s_1 = times[(df_line['direction']==1) & (df_line['section']==1)]
    plt.scatter(buses_s_1, times_s_1, marker='x', c='blue', s=size, alpha=alpha)
    buses_s_2 = buses[(df_line['direction']==2) & (df_line['section']==1)]
    times_s_2 = times[(df_line['direction']==2) & (df_line['section']==1)]
    plt.scatter(buses_s_2, times_s_2, marker='x', c='orange', s=size, alpha=alpha)
    mpl.rcParams['figure.figsize'] = (6, 7)
    plt.xticks(range(len(unique_a)), unique_a, rotation=90)
    plt.yticks(range(3,28))
    plt.ylim((6,24))
    font = FontProperties(fname="C:/Windows/Fonts/simhei.ttf", size=14)
    plt.title(f"{lineName} {datestr}", fontproperties=font)
    
    plt.tight_layout()
    return len(unique_a)


def analyzeDayLine(datestr=None):
    if datestr is None:
        datestr = datetime.now().strftime('%y%m%d')
    df = readDayData(datestr)
    linecode = pd.read_csv('E:/real/src/lineCodes.csv', header=None)
    lineNameList = linecode[0].to_list()
    for lineName in lineNameList:
        plotDayLine(lineName, df, datestr)
        plt.savefig(f"E:/xianbus/{datestr}/line/{lineName}.png")
        print(f'saved {lineName}')
        plt.close()

def plotDayBus(bus=None, df = None, datestr=None):
    if df is None:
        df = readDayData()
    assert df is not None, "df is None"
    size = 17
    alpha = 0.8
    df_bus = df[df['bus'] == bus].copy()
    df_bus['direction'] = df_bus['direction'].astype(str)
    df_bus['section'] = df_bus['section'].astype(str)
    df_bus['line'] = df_bus['line'] + df_bus['section'] + df_bus['direction']
    df_bus = df_bus.drop(['bus'], axis=1)
    df_bus["a_numeric"], unique_a = pd.factorize(df_bus["line"], sort=True)
    mpl.rcParams['figure.figsize'] = (6, 7)
    plt.scatter(df_bus["a_numeric"], df_bus["time"], s=size, alpha=alpha)
    plt.xticks(range(len(unique_a)), unique_a, fontproperties=font)
    # y_ticks = list(range(0,25)) + ['1','2','3']
    plt.yticks(range(3,28))
    plt.ylim((6,24))
    plt.title(f"{bus} {datestr}", fontproperties=font)
    plt.tight_layout()
    return(len(unique_a))

def generate_markdown_file():
    SRC_PATH = 'E:/real/src'
    linecode = pd.read_csv(f'{SRC_PATH}/lineCodes.csv', header=None)
    lineNameList = linecode[0].to_list()
    filename='E:/xianbus/index.md'
    SRC_PATH = 'E:/real/6190/src'
    linecode = pd.read_csv(f'{SRC_PATH}/lineCodes.csv', header=None)
    lineNameList = lineNameList + linecode[0].to_list()

    datestr = datetime.now().strftime('%y%m%d')
    # datestr = '241121'
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(f'## [today]({datestr})\n')
        file.write(f'<!--\n')
        for i in range(len(lineNameList)):
            line = lineNameList[i]
            file.write(f"[{line}](line/{line}.png)\n")
    filename=f'E:/xianbus/{datestr}/index.md'
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(f'# xianbus today: {datestr}\n')
        for i in range(len(lineNameList)):
            line = lineNameList[i]
            file.write(f"[{line}]({datestr}/line/{line}.png)\n")

if __name__ == "__main__":
    # analyzeLine()
    # analyzeDayLine()
    generate_markdown_file()