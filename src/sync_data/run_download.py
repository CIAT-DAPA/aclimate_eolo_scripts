import argparse

from download_data import DownloadData
from get_date_geoserver import GetDateGeoserver
from create_climatology import  CreateClimatology

def main():
    # Params
    # 0: URL
    # 1: Path
    # 2: File Name
    # 3: Target Name
    # 4: GeoServer URL
    # 5: GeoServer Workspace
    # 6: GeoServer User
    # 7: GeoServer Password
    # 8: Process

    parser = argparse.ArgumentParser(description="Download tif script")

    parser.add_argument("-u", "--url", help="URL from where the data will be downloaded")
    parser.add_argument("-p", "--path", help="Path where the data will be saved")
    parser.add_argument("-f", "--file", help="Name that the file will have followed by the date PREC_yyyyMM.tif")
    parser.add_argument("-t", "--target", help="Name of the file that will be downloaded to filter the files")
    parser.add_argument("-g", "--geo", help="GeoServer URL")
    parser.add_argument("-w", "--workspace", help="GeoServer workspace")
    parser.add_argument("-usr", "--user", help="GeoServer user")
    parser.add_argument("-pass", "--password", help="GeoServer password")
    parser.add_argument("-cp", "--climpath", help="Path where the climatology data will be saved")
    parser.add_argument("-prc", "--process", help="1: Download historical data, 2: Create climatology, 3: Run both processes", type=int, required=True)

    args = parser.parse_args()

    print("Reading inputs")
    print(args)

    process = args.process

    if process == 1:
        if not (args.geo and args.workspace and args.url and args.path and args.file and 
                args.target and args.user and args.password):
            parser.error("For process 1, arguments -u, -p, -f, and -t are required.")

        geo = GetDateGeoserver(args.geo, args.workspace, args.file, args.user, args.password)
        start_date = geo.start_date if geo.start_date else "1981-01"

        ar = DownloadData(args.url, args.path, args.file, start_date, args.target)
        ar.main()
    elif process == 2:
        if not (args.geo and args.workspace and args.file and args.user and args.password and args.path):
            parser.error("For process 2, arguments -g, -w, -f, -usr, -pass, and -p are required.")

        cl = CreateClimatology(args.geo, args.workspace, args.file, 
                               args.user, args.password, args.path,
                                [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
        cl.main()
    elif process == 3:
        if not (args.geo and args.workspace and args.url and args.path and args.file and 
                args.target and args.user and args.password and args.climpath):
            parser.error("For process 3, all arguments are required.")

        geo = GetDateGeoserver(args.geo, args.workspace, args.file, args.user, args.password)
        start_date = geo.start_date if geo.start_date else "1981-01"

        ar = DownloadData(args.url, args.path, args.file, start_date, args.target)
        ar.main()
        print(ar.get_unique_months_in_folder(args.path))

        cl = CreateClimatology(args.geo, args.workspace, args.file, 
                               args.user, args.password, args.climpath,
                                ar.months)
        cl.main()
    else:
        parser.error("Invalid process number. Please provide either 1, 2, or 3.")

if __name__ == "__main__":
    main()



    # -u "https://data.chc.ucsb.edu/experimental/CHIRP-n-CHIRPS_v3_beta/CHIRPS/beta-3.2/monthly/camer-carib_tifs/" 
    # -p "D:\Code\download_historical_data\data" 
    # -f "PREC" -t "beta.chirps-v3.2" 
    # -g "https://geo.aclimate.org/geoserver/" 
    # -w "historical_climate_hn" 
    # -usr "scalderon" 
    # -pass "Santi2711."