import json, os
import boto3
import jenkspy
import pandas as pd
import tempfile
from .spatial import translate_position


TRY_ENCODINGS = [
    'utf-8-sig',
    'cp1252',  # ANSI
    'latin-1',
    'ascii'
]


def csv_to_df(file, encoding='utf-8-sig', dtype=None):
    def read_csv(file, encoding, dtype=None):
        try:
            return pd.read_csv(file, encoding=encoding, dtype=dtype)
        except UnicodeDecodeError as e:
            for enc in TRY_ENCODINGS:
                try:
                    return pd.read_csv(file, encoding=enc, dtype=dtype)
                except UnicodeDecodeError:
                    pass
            raise e

    if hasattr(file, 'save'):
        with tempfile.TemporaryDirectory() as tmpdir:
            fpath = os.path.join(tmpdir, file.filename)
            file.save(fpath)
            return read_csv(fpath, encoding, dtype=dtype)

    return read_csv(file, encoding, dtype=dtype)

"""
# what an interesting format. Example:

* AERMOD (22112 ): 261658229211                                                             
* AERMET ( 15181):                                                                          
* MODELING OPTIONS USED:   NonDFAULT  DDEP  WDEP  FLAT and  ELEV  DRYDPLT  WETDPLT  ALPHA  RURA
*         PLOT FILE OF PERIOD VALUES AVERAGED ACROSS   0 YEARS FOR SOURCE GROUP: CEIM0010
*         FOR A TOTAL OF   631 RECEPTORS.
*         FORMAT: (2(1X,F13.5),2(1X,E13.6),3(1X,F8.2),2X,A6,2X,A8,2X,I8.8,2X,A8)
*        X             Y          DRY DEPO      WET DEPO    ZELEV    ZHILL    ZFLAG    AVE
* ____________  ____________  ____________  ____________   ______   ______   ______  ______
  626981.00000 4902622.00000  0.437213E-06  0.122109E-05   394.50   394.50     0.00  PERIOD
  626981.00000 4902712.00000  0.131317E-05  0.729148E-06   395.90   397.50     0.00  PERIOD
  626981.00000 4902862.00000  0.207727E-05  0.441198E-06   394.70   394.70     0.00  PERIOD
  626981.00000 4903112.00000  0.180702E-05  0.268801E-06   394.10   394.10     0.00  PERIOD
  626981.00000 4903532.00000  0.110551E-05  0.161837E-06   393.90   393.90     0.00  PERIOD
  626981.00000 4904232.00000  0.640101E-06  0.973802E-07   394.40   394.40     0.00  PERIOD
 
see column Y; values can precede the "start" of the underscores!
Safest approach I think is look for the end of a column and then take everything +1 as the next column
"""
def parse_plt_file(raw_data):
    # we'll return this "parsed" dictionary. If ever useful, could also return stuff like the derived columns,
    # or things like the "modeling options used" that appear in the comment line
    # but the parsed data is probably all we truly care about.
    parsed = [] # one entry per data row of file. Each entry is dictionary containing:
                # "data" - dictionary, colnames as keys. casted/cleaned/processed data (e.g. "00087" appears
                #          as a numpy.int64 with value 87.
                # "original_data" - dictionary, colnames as keys. raw data straight from the file (e.g. "00087"
                #                   appears as a string with value "00087" 
                # "raw_line" - string of the line as it literally appeared in the file
                # "line_number_in_file" - line # of the line in the file it came from. Useful for
                #                          debugging/troubleshooting.

    if raw_data.endswith("\r\n"):
        lines = raw_data.split("\r\n")
    elif raw_data.endswith("\n"):
        lines = raw_data.split("\n")
    elif raw_data.endswith("\r"):
        lines = raw_data.split("\r")
    else:
        raise Exception("Unable to determine line ending for plt data")

    line_num = 1
    header_underscore_line = None
    for line in lines:
        if line.startswith("* __"):
            header_underscore_line = line_num
            break
        line_num += 1

    underscores_raw = lines[header_underscore_line-1]
    names_raw = lines[header_underscore_line-2]

    # figure out column widths
    start_from = 0
    cols = [] # store name, start, end of each column
    while True:
        us_pos = underscores_raw.find("_", start_from) # underscore_position

        if us_pos == -1:
            break

        space_pos = underscores_raw.find(" ", us_pos)

        name_probe = names_raw[start_from:] if space_pos == -1 else names_raw[start_from:space_pos]
        name_probe = name_probe.strip()
        if name_probe.startswith("* "):
            name_probe = name_probe[1:].strip().upper()

        if space_pos == -1:
            cols.append((name_probe, start_from, len(underscores_raw)))
            break
        else:
            cols.append((name_probe, start_from, space_pos-1))

        start_from = space_pos
        
    # now parse the individual lines

    # try to convert to a number using pandas utils. Could add special "by column" overrides if needed,
    # but this works decently already.
    def convert_data(col_name, raw_val):
        try:
            return pd.to_numeric(raw_val)
        except:
            return raw_val

    data_lines = 0
    for line in lines[header_underscore_line:]:
        if line.strip() == "":
            break
 
        line_number_in_file = 1 + header_underscore_line + data_lines
        # print(f"[DATA LINE #{data_lines+1}] / [LINE NUMBER {line_number_in_file}]")

        slotted_data = {}
        original_data = {}
        for col_name, col_start, col_end in cols:
            cell_data = (line[col_start:col_end+1]).strip()
            slotted_data[col_name] = convert_data(col_name, cell_data)
            original_data[col_name] = cell_data

        parsed.append({ "data": slotted_data, "original": original_data, "raw_line": line, "line_number_in_file": line_number_in_file})

        data_lines += 1

    # return column names too
    return parsed, [ x[0] for x in cols ]

def parse_plt_file_as_dataframe(raw_data):
    parsed, _ = parse_plt_file(raw_data)
    return pd.DataFrame([p["data"] for p in parsed])


class MiscAssociatedFileVariety():
    MIME_TYPE = "text/plain"
    STORAGE_EXTENSION = None

    @classmethod
    def construct_file_variety(cls, variety_name):
        # eventually -- make this less hardcoded? but right now only one variety so keep it simple and make it better
        # when/if we add another.
        if variety_name == "deposition_overlay":
            return MiscAssociatedFileDepositionOverlay(variety_name)
        elif variety_name == "generated_aermod_receptors":
            return MiscAssociatedFileAERMODGeneratedReceptors(variety_name)

        # return basic/generic variety
        return MiscAssociatedFileVariety(variety_name)

    def __init__(self, variety_name):
        self.variety = variety_name

    def get_storage_mime_type(self):
        return self.MIME_TYPE

    def get_storage_file_extension(self):
        return "" if self.STORAGE_EXTENSION is None else f".{self.STORAGE_EXTENSION}"

    def has_custom_upload_behavior(self):
        custom_fxn = getattr(self, "perform_custom_upload_behavior", None)
        return callable(custom_fxn)

    def get_files_to_suppress_from_download(self):
        return []

    # if implemented in subclass, should return a tuple
    # first element is a dictionary of filenames: dict
    #       each sub-dict should contain the contents of the file to upload and the mime type.
    #       (if you omit mime it will use the MIME_TYPE on the class)
    # second element is a dictionary of additional metadata items we want to store on S3, beyond the defaults. (Or None)
    # def perform_custom_upload_behavior(self, **kwargs):

class MiscAssociatedFileDepositionOverlay(MiscAssociatedFileVariety):

    def apply_GRP_logic(self, df, input_file_errors):
        if "GRP" in df.columns.to_list():
            unique_group_names = df["GRP"].unique()
            if len(unique_group_names) == 1:
                # only one group; ok to use it
                pass
            else:
                if "ALL" in unique_group_names:
                    # drop all rows where "GRP" != "ALL" (tilde negates)
                    df = df.drop(df[~(df["GRP"] == "ALL")].index)
                else:
                    input_file_errors.append("Multiple GRP entries found; none were ALL")
        else:
            input_file_errors.append("No GRP column found")
        # latest guidance -- since using either single GRP or GRP==ALL, no need
        # to additionally pandas.groupby on x/y; the GRP logic we're employing
        # handles that issue
    
    def apply_ZFLAG_logic(self, df, input_file_errors, metadata):
        try:
            zflag_restriction = float(metadata.get("zflag_restriction"))
        except:
            zflag_restriction = None

        if "ZFLAG" in df.columns.to_list():
            unique_zflag_vals = df["ZFLAG"].unique()
            if len(unique_zflag_vals) == 1:
                # only one zflag; ok to use it
                pass
            else:
                if 0 in unique_zflag_vals:
                    # drop all rows where "ZFLAG" != 0 (tilde negates)
                    df = df.drop(df[~(df["ZFLAG"] == 0)].index)
                else:
                    if zflag_restriction is not None:
                        # filter to only include thise
                        df = df.drop(df[~(df["ZFLAG"] == zflag_restriction)].index)
                    else:
                        input_file_errors.append(f"ZFLAG issues")

    def perform_custom_upload_behavior(self, **kwargs):
        if "uploaded_contents" in kwargs and "metadata" in kwargs:
            metadata = kwargs.get("metadata")
            uploaded_contents = kwargs.get("uploaded_contents")
            df = parse_plt_file_as_dataframe(uploaded_contents)
            plt_cols = df.columns.to_list()

            input_file_errors = []
            break_metadata = []
            additional_metadata = {}

            # translate uploaded coords to WGS84 LONGLAT
            translation_needed = False
            if metadata.get("coord_system", "").upper().startswith("WGS84 LONG"):
                pass
            elif metadata.get("coord_system", "").upper() == "UTM":
                translation_needed = True

            # first three exist in the input file...
            DRY_DEPO_COL = "DRY DEPO"
            WET_DEPO_COL = "WET DEPO"
            TOTAL_DEPO_COL = "TOTAL DEPO"
            COMBINED_DEPO_COL = "combined_deposition" # this one we'll generate

            if len(df) == 0:
                input_file_errors.append("No data rows")
            else:
                if TOTAL_DEPO_COL not in plt_cols and DRY_DEPO_COL not in plt_cols and WET_DEPO_COL not in plt_cols:
                    input_file_errors.append("missing 'TOTAL DEPO' / 'DRY DEPO' / 'WET DEPO'")

            # apply some bizlogic rules based on GRP and ZFLAG cols
            if len(input_file_errors) == 0:
                self.apply_GRP_logic(df, input_file_errors)
                self.apply_ZFLAG_logic(df, input_file_errors, metadata)

            # sum up deposition
            if len(df) > 0:
                if TOTAL_DEPO_COL not in plt_cols:
                    cols_to_sum = [x for x in [DRY_DEPO_COL, WET_DEPO_COL] if x in plt_cols]
                    df[COMBINED_DEPO_COL]= df[cols_to_sum].sum(axis=1)
                else:
                    df[COMBINED_DEPO_COL] = df["TOTAL DEPO"]
            else:
                input_file_errors.append("No data rows after GRP/ZFLAG filtering")

            # ensure df has wgs84_long/lat columns, either via translation or raw supplied values
            if len(input_file_errors) == 0:
                if translation_needed:
                    # translate X/Y to lat/lng
                    utm_zone = metadata.get("utm_zone")
                    df["wgs84_long"] = df.apply(lambda row: translate_position(row.X, row.Y, "UTM", "WGS84_LONGLAT", utm_zone=utm_zone)[0], axis = 1)
                    df["wgs84_lat"] = df.apply(lambda row: translate_position(row.X, row.Y, "UTM", "WGS84_LONGLAT", utm_zone=utm_zone)[1], axis = 1)
                else:
                    # just use X/Y as-is
                    df["wgs84_long"] = df["X"]
                    df["wgs84_lat"] = df["Y"]

            # apply jenks bucketing
            if len(input_file_errors) == 0:
                num_jenks_buckets = 4
                breaks = jenkspy.jenks_breaks(df[COMBINED_DEPO_COL], n_classes=num_jenks_buckets)
                labels = [x for x in range(0,num_jenks_buckets)]
                df['jenks_bucket'] = pd.cut(df[COMBINED_DEPO_COL], bins=breaks, labels=labels, include_lowest=True)
                for i in range(0, len(breaks)-1):
                    break_metadata.append({ "from": breaks[i], "to": breaks[i+1] })

            packaged_data = {
            }

            if len(input_file_errors) == 0:
                # return just a subset of the dataframe we've worked on
                desired_cols = [
                    "wgs84_long",
                    "wgs84_lat",
                    "jenks_bucket",
                    COMBINED_DEPO_COL
                ]
                cols_to_return = [ col_name for col_name in desired_cols if col_name in df.columns.to_list() ]
                df = df[cols_to_return]

                packaged_data["row_data"] = df.to_dict(orient="records")
                additional_metadata["jenks_buckets"] = break_metadata
            else:
                packaged_data["row_data"] = []
                additional_metadata["errors"] = input_file_errors

            return ({
                "original.plt": { "contents": uploaded_contents, "mime": "text/plt" },
                "processed.json": { "contents": json.dumps(packaged_data), "mime": "application/json" }
            }, additional_metadata)
        else:
            raise Exception(f"{self.__class__}.perform_custom_upload_behavior expected 'uploaded_contents' and 'metadata' in kwargs but was missing one or more of them")


    def get_files_to_suppress_from_download(self):
        return ["original.plt"]

class MiscAssociatedFileAERMODGeneratedReceptors(MiscAssociatedFileVariety):
    MIME_TYPE = "application/geojson"
    STORAGE_EXTENSION = "geojson"

    # we already have this data in memory, no need to open it
    # like w/ MiscAssociatedFileDepositionOverlay custom code.
    # this is instead of implementing
    # perform_custom_upload_behavior for this class.
    def convert_grid_point_data_to_binary_geojson(self, grid_point_data):
        # PART 1: we want to make something like this:
        """
        {
        "type": "FeatureCollection",
        "name": "output_grid_points_all",
        "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },
        "features": [
        { "type": "Feature", "properties": { "parcel_id": 0, "spacing_m": 100 }, "geometry": { "type": "Point", "coordinates": [ -85.421154684715873, 44.234350919704234 ] } },
        { "type": "Feature", "properties": { "parcel_id": 0, "spacing_m": 100 }, "geometry": { "type": "Point", "coordinates": [ -85.420256369431755, 44.233707280018194 ] } },
        ...
        ] }
        """

        reformatted = {
            "type": "FeatureCollection",
            "name": "trim_generated_aermod_receptors",
            "crs": {
                "type": "name",
                "properties": {
                    "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
                }
            },
            "features": []
        }

        for gpd in grid_point_data:
            parcel_id = gpd.get("parcel_id")
            spacing_m = gpd.get("spacing_m")
            long_lat_pairs = gpd.get("long_lat_pairs")
            for pair in long_lat_pairs:
                feature = {
                    "type": "Feature",
                    "properties": {
                        "parcel_id": parcel_id,
                        "spacing_m": spacing_m
                    },
                    "geometry": {
                        "type": "Point",
                        "coordinates": [
                            pair[0],    # longitude
                            pair[1]     # latitude
                        ]
                    }
                }
                reformatted["features"].append(feature)

        # PART 2: we want this to be a file-like object so
        # that we can leverage the built-in file upload code
        # return reformatted
        return json.dumps(reformatted).encode("utf-8")


# non-api-specific utility function that retrieves/uploads/deletes a
# MiscAssociatedFileVariety file. refactored from the "manage_misc_scenario_file"
# endpoint/route handler
def associated_file_helper(scenario_id, misc_file_type:str, operation:str, file_obj = None, file_metadata=None):

    print(f"ASSOCIATED FILE HELPER REFACTORIZATION: {scenario_id=}, {misc_file_type=}, {operation=}")
    # this function leverages the MiscAssociatedFileVariety class hierarchy defined in ../utils/file_io.py; provides basic defaults as
    # described above for "store this file on S3 and do nothing else" but can also provide custom behavior easily like preprocessing a file, setting
    # smarter MIME/content type, etc. For instance the "deposition_overlay" misc_file_type/variety:
    # 1. processes the uploaded file
    # 2. stores both the original uploaded file (just in case / proof-of-concept) and the processed version
    # 3. returns presigned url for just the processed version on a GET
    #
    # initially this is only used for those aermod deposition overlays on the parcels tab, but it could be used in other places going forward.
    rv = {}
    operation = operation.upper()
    if operation not in ["DELETE", "CHECK", "UPLOAD"]:
        raise Exception(f"Unsupported file op '{operation}'")

    print("REFACTORED ASSOCIATED_FILE_HELPER HERE WE GO!")
    file_storage_bucket = os.getenv("SCENARIO_MISC_FILES_BUCKET_NAME")

    s3_client = boto3.client("s3")
    s3_resource = boto3.resource("s3")

    fv = MiscAssociatedFileVariety.construct_file_variety(misc_file_type)

    s3_metadata_path = f"{scenario_id}/{misc_file_type}/_metadata.json"

    print(f"bucket={file_storage_bucket}; metadata {s3_metadata_path}")

    do_return_metadata_and_presigned_urls = False
    if operation == "DELETE":
        bucket = s3_resource.Bucket(file_storage_bucket)
        bucket.objects.filter(Prefix=f"{scenario_id}/{misc_file_type}/").delete()
        rv["delete_operation"] = True
    elif operation == "CHECK":
        do_return_metadata_and_presigned_urls = True
    elif operation == "UPLOAD":
        try:
            if fv.has_custom_upload_behavior():
                fpn = file_obj.stream
                try:
                    fpn.seek(0)
                    uploaded_file_content = fpn.read().decode("utf-8")

                    upload_directives, additional_metadata = fv.perform_custom_upload_behavior(uploaded_contents=uploaded_file_content, metadata=file_metadata)
                    for upload_filename in upload_directives:
                        uploadable_dict = upload_directives[upload_filename]
                        uploadable_item = uploadable_dict.get("contents")
                        uploadable_mime = uploadable_dict.get("mime", fv.get_storage_mime_type())
                        loop_s3_file_path = f"{scenario_id}/{misc_file_type}/{upload_filename}"

                        s3_client.put_object(
                            Body=uploadable_item,
                            Bucket=file_storage_bucket,
                            Key=loop_s3_file_path,
                            ContentType=uploadable_mime
                        )

                    if additional_metadata is not None:
                        file_metadata = file_metadata | additional_metadata
                except Exception as e:
                    raise Exception(e)
            else:
                s3_file_path = f"{scenario_id}/{misc_file_type}/data{fv.get_storage_file_extension()}"

                s3_client.put_object(
                    Body=file_obj,
                    Bucket=file_storage_bucket,
                    Key=s3_file_path,
                    ContentType=fv.get_storage_mime_type()
                )

            # update the metadata too - for default or custom
            s3_client.put_object(
                Body=json.dumps(file_metadata),
                Bucket=file_storage_bucket,
                Key=s3_metadata_path,
                ContentType="application/json"
            )

            do_return_metadata_and_presigned_urls = True
        except Exception as e:
            raise Exception(e)

    print(f"past first section; {do_return_metadata_and_presigned_urls=}")

    if do_return_metadata_and_presigned_urls:
        file_metadata = None
        try:
            content_object = s3_resource.Object(file_storage_bucket, s3_metadata_path)
            file_content = content_object.get()["Body"].read().decode("utf-8")
            file_metadata = json.loads(file_content)
        except:
            file_metadata = None
        
        if file_metadata is not None:
            rv["file_metadata"] = file_metadata
        else:
            rv["file_metadata"] = None

        # now make presigned urls
        rv["presigned_urls"] = {}
        try:
            # get everythign in the appropriate subdir
            response = s3_client.list_objects_v2(
                    Bucket=file_storage_bucket,
                    Prefix = f"{scenario_id}/{misc_file_type}/",
                    MaxKeys=100 )

            s3_files = response.get("Contents", [])
            for f in s3_files:
                suppressed_files = fv.get_files_to_suppress_from_download()

                loop_key = f.get("Key")
                if loop_key != s3_metadata_path:
                    nested_path = loop_key.replace(f"{scenario_id}/{misc_file_type}/", "")

                    if nested_path not in suppressed_files:
                        data_url = s3_client.generate_presigned_url("get_object",
                                                                    Params={
                                                                        "Bucket": file_storage_bucket,
                                                                        "Key": loop_key
                                                                    },
                                                                    ExpiresIn=600) # expires in 10 minute(s)
                        rv["presigned_urls"][nested_path] = data_url
        except Exception as e:
            raise Exception(e)

    return rv
