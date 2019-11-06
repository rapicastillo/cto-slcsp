import csv


PLANS_CSV = './plans.csv'
ZIPCODE_CSV = './zips.csv'
SLCSP_CSV = './slcsp.csv'
RESULTS_CSV = './slcsp_results.csv'

# First step is to process the slcsp for each rate_area
# storing them in a dict with keys of rate area to list of the lowest two rates
# which will be updated as we go through plans csv
def get_slcsp_per_rate_area():
    slcsp_list = dict()
    with open(PLANS_CSV) as csv_file:

        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader) # skip head
        for row in csv_reader:
            metal_level = row[2]
            rate = row[3]
            state = row[1]
            rate_area = row[4]

            rate_area_key = "%s %s" % (state, rate_area)
            rate = float(rate)
            if rate_area_key not in slcsp_list:
              slcsp_list[rate_area_key] = []
              slcsp_list[rate_area_key].append(rate)

            # In this area, we will check if the rate area only has one inetry, in which case, we append the rate
            elif len(slcsp_list[rate_area_key]) == 1:
                if rate < slcsp_list[rate_area_key][0]:
                    slcsp_list[rate_area_key].insert(0, rate)
                else:
                    slcsp_list[rate_area_key].append(rate)

            # This updates the rate areas' 2 lowest rates.
            elif len(slcsp_list[rate_area_key]) > 1:
                if rate < slcsp_list[rate_area_key][0]:
                    slcsp_list[rate_area_key].insert(0, rate)
                    del slcsp_list[rate_area_key][-1]
                elif rate > slcsp_list[rate_area_key][0] and rate < slcsp_list[rate_area_key][1]:
                    slcsp_list[rate_area_key].insert(1, rate)
                    del slcsp_list[rate_area_key][-1]
    return slcsp_list

# This processes the zips.csv file and assigns all the rate areas allocated to a zip
def get_rate_area_zip():
    zip_list = dict()
    with open(ZIPCODE_CSV) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader) # skip head
        for row in csv_reader:
            zipcode = row[0]
            state = row[1]
            rate_area = row[4]
            rate_key = "%s %s" % (state, rate_area)

            if zipcode not in zip_list:
                zip_list[zipcode] = []
                
            if rate_key not in zip_list[zipcode]:
                zip_list[zipcode].append(rate_key)
    
    return zip_list

# This method makes the actual matching of zipcode and geetting the second lowest rate for an arae
def get_slcsp(slcsp_list, zip_list):
    zip_results = []
    with open(SLCSP_CSV) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader) # skip head
        for row in csv_reader:
            zipcode = row[0]
            if zipcode in zip_list:
                rate_areas = zip_list[zipcode]
                if len(rate_areas) == 1:
                    rate_area = rate_areas[0]
                    if rate_area in slcsp_list:
                        zip_results.append(dict(
                          zipcode=zipcode,
                          rate=slcsp_list[rate_area][1] if len(slcsp_list[rate_area]) > 1 else None 
                        ))
                    else: 
                        zip_results.append(dict(
                          zipcode=zipcode,
                          rate=None
                        ))
                else:
                    zip_results.append(dict(
                        zipcode=zipcode,
                        rate=None
                    ))

    return zip_results

# This writes the results onto a csv file
def write_results(slcsp_results):
    with open(RESULTS_CSV, mode='w') as slcsp_writer:
        writer = csv.writer(slcsp_writer, delimiter=",")
        writer.writerow(["zipcode", "rate"])

        for item in slcsp_results:
            writer.writerow([item['zipcode'], item['rate'] if item['rate'] is not None else ''])
            

def main():
    slcsp_list = get_slcsp_per_rate_area()
    zip_list = get_rate_area_zip()
    slcsp = get_slcsp(slcsp_list, zip_list)
    write_results(slcsp)

if __name__ == "__main__":
    main()