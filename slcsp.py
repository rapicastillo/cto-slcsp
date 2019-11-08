import csv

class AreaRates():
    """
    This class will always have the 2 lowest rates of any given rate area, 
    it's updated through the add_rate method
    """

    def __init__(self):
        self.rates = dict()
    
    def __update_rates(self, area_rates, rate):
        """
        This private method will check if the new rate can replace the 
        current rates. They can replace it if it's lower either of the rates
        """
        size = len(area_rates)
        if size == 0:
            area_rates = [rate]
        elif size == 1:
            insert_at = 0 if rate < area_rates[0] else 1
            area_rates.insert(insert_at, rate)
        elif rate < area_rates[1] and not rate == area_rates[0]:
            # If len(area_rates) > 1 and it's less than the second element
            # we then compare it with the first element to figure out where to
            # insert the rate, then delete the last element
            insert_at = 0 if rate < area_rates[0] else 1
            area_rates.insert(insert_at, rate)
            del area_rates[-1]

        return area_rates

    def get_slcsp(self, rate_area):
        """
        This will get the SLCSP for a given rate_area
        """
        rates = self.rates.get(rate_area, [])
        if len(rates) != 2:
            return None
        else:
            # The second rate will always be the SLCSP
            return rates[1] 
        
        
    def add_rate(self, rate_area, rate):
        area_rates = self.rates.get(rate_area, [])
        new_rates = self.__update_rates(area_rates, rate)
        self.rates[rate_area] = new_rates

    def get_rates_list(self):
        return self.rates




class SLCSPFinder():
    # Files
    PLANS_CSV = './plans.csv'
    ZIPCODE_CSV = './zips.csv'
    SLCSP_CSV = './slcsp.csv'

    def __init__(self):
        self.zip_list = dict()
        self.area_rates = AreaRates()

    def run(self):
        self.__process_rates_per_rate_area()
        self.__process_rate_area_zip()
        results = self.__process_slcsp()
        return results

    def __process_rates_per_rate_area(self):
        """
        First step is to process the slcsp for each rate_area
        storing them in a dict with keys of rate area to list of the lowest two rates
        which will be updated as we go through plans csv
        """
        with open(self.PLANS_CSV) as csv_file:

            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader) # skip head
            for row in csv_reader:
                metal_level = row[2]
                rate = row[3]
                state = row[1]
                rate_area = row[4]

                rate_area_key = "%s %s" % (state, rate_area)
                rate = float(rate)

                self.area_rates.add_rate(rate_area_key, rate)


    
    def __process_rate_area_zip(self):
        """
        This processes the zips.csv file and 
        assigns all the rate areas allocated to a zip
        """
        with open(self.ZIPCODE_CSV) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader) # skip head
            for row in csv_reader:
                zipcode = row[0]
                state = row[1]
                rate_area = row[4]
                rate_key = "%s %s" % (state, rate_area)

                if zipcode not in self.zip_list:
                    self.zip_list[zipcode] = []
                    
                if rate_key not in self.zip_list[zipcode]:
                    self.zip_list[zipcode].append(rate_key)

    
    def __process_slcsp(self):
        """
        This method makes the actual matching of zipcode and 
        getting the second lowest rate for an area
        """
        zip_results = []
        with open(self.SLCSP_CSV) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader) # skip head
            for row in csv_reader:
                zipcode = row[0]
                rate_area = self.zip_list.get(zipcode, [])
                slcsp = None if len(rate_area) != 1 else self.area_rates.get_slcsp(rate_area[0])
                zip_results.append(dict(zipcode=zipcode, rate=slcsp))

        return zip_results


    def write_results(self, slcsp_results, destination):
        """
        This writes the results onto a csv file
        """
        with open(destination, mode='w') as slcsp_writer:
            writer = csv.writer(slcsp_writer, delimiter=",")
            writer.writerow(["zipcode", "rate"])

            for item in slcsp_results:
                writer.writerow([item['zipcode'], item['rate'] if item['rate'] is not None else ''])
            

RESULTS_CSV = './slcsp_results.csv'
def main():
    slcsp_finder = SLCSPFinder()
    results = slcsp_finder.run()

    slcsp_finder.write_results(results, RESULTS_CSV)
    

if __name__ == "__main__":
    main()