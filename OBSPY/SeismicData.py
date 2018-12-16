class SeismicData():
    def __init__(self, station_data):
        self.__station_data = station_data
        self.alive_traces_with_times = []
        self.alive_traces_count = []
        self.__station_data_preprocessing(station_data)
    def calculate_live_traces(self):
        print('Calculating number of alive traces...')
        for cur_index, time in enumerate(self.times):
            alive_traces = 0
            for trace in self.traces:
                if type(trace.data[cur_index]) != type(None):
                    alive_traces+=1
            self.alive_traces_with_times.append((time, alive_traces))
        for alive_trace in self.alive_traces_with_times:
            self.alive_traces_count.append(alive_trace[1])
        print('Calculating number of alive traces finished')
    def plot_station_data(self):
        self.__station_data.plot()
    def convert_to_csv(self, file_name="seismic_data.csv"):
        print('Converting object to matrix...')
        self.calculate_live_traces()
        all_data = []
        for trace in self.traces:
            print(trace)
            all_data.append(trace.data)
        all_data.append(self.times)
        all_data.append(self.alive_traces_count)
        df = pd.DataFrame([np.array(all_data)])
        df.to_csv(file_name)
        print('Converting object to matrix finished')
    def __trace_preprocessing(self, target_trace, canonical_times, npts):
        print('Trace preprocessing...')
        if(len(target_trace.data) < len(canonical_times)):
            target_times = target_trace.times('utcdatetime')
            target_trace.stats.starttime = canonical_times[0]
            target_trace.stats.npts = npts
            indexes = len(canonical_times) - len(target_times)
            zeros = np.zeros([indexes])
            new = np.hstack([zeros,target_trace.data])
            target_trace.data = new
        print('Trace preprocessing finished')
    
    def __station_data_preprocessing(self, station_data):
        print('Station data preprocessing...')
        max_trace = None
        max_len = 0
        for trace in station_data.traces:
            if len(trace.data) > max_len:
                max_len = len(trace.data)
                max_trace = trace
        print('max trace = {0}'.format(max_trace))
        max_times = max_trace.times('utcdatetime')
        print('max trace times = {0}'.format(max_times))
        for trace in station_data.traces:
            self.__trace_preprocessing(trace, max_times, max_trace.stats.npts)
        
        self.__station_data = station_data
        self.traces = station_data.traces
        self.times = station_data[0].times('utcdatetime')
        self.starttime = self.times[0]
        self.endtime = self.times[len(self.times)-1]
        self.calculate_live_traces()
        
        print('Station data preprocessing finished')