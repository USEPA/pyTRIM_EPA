import time
import requests
import xmltodict
from ...utils.logging import make_logger


class ApiMeta(type):
    _headers = {
        'Authorization': None
    }
    _session = None

    @property
    def root(cls):
        return 'https://sdmdataaccess.sc.egov.usda.gov/Tabular/SDMTabularService.asmx'

    @property
    def headers(cls):
        return cls._headers

    @property
    def session(cls):
        if cls._session is None:
            cls._session = requests.Session()
        cls._session.headers.update(cls.headers)
        return cls._session


class UsdaApi(metaclass=ApiMeta):
    @classmethod
    def get_parcel_soil_data(cls, parcel_name, parcel_coords, username=None, password=None):
        cls.headers['Content-Type'] = 'text/xml'
        vertex = parcel_coords
        query = f'-- Define a triangular AOI in WGS84\n\
~DeclareGeometry(@aoi)~\n\
-- Parcel W1 of Foundries\n\
select @aoi = geometry::STPolyFromText(\'polygon((\
{vertex} \
))\', 4326) \n\
-- Extract all intersected polygons\n\
~DeclareIdGeomTable(@intersectedPolygonGeometries)~\n\
~GetClippedMapunits(@aoi,polygon,geo,@intersectedPolygonGeometries)~\n\
-- select * from @intersectedPolygonGeometries\n\
-- Convert geometries to geographies so we can get areas\n\
~DeclareIdGeogTable(@intersectedPolygonGeographies)~\n\
~GetGeogFromGeomWgs84(@intersectedPolygonGeometries,@intersectedPolygonGeographies)~\n\
-- get aggregated areas and associated mukey, musym, nationalmusym, areasymbol, mucertstat (Map Unit Certification Status)\n\
select id, sum(geog.STArea()) as area\n\
into #aggarea from @intersectedPolygonGeographies\n\
group by id;\n\
-- ~DeclareFloat(@sumArea)~\n\
-- select @sumArea = sum(A.area)\n\
-- from #aggarea A\n\
-- select @sumArea\n\
-- Return the polygons with joined data\n\
select M.mukey, A.area, C.hzname, C.hzdept_r, C.hzdepb_r, C.hzthk_r, Co.compname, Co.comppct_r, Co.slope_r, C.kwfact, C.ph1to1h2o_r, C.om_r, C.awc_r, C.sandtotal_r, Co.slopelenusle_r\n\
--select M.mukey, A.area, C.*, Co.*\n\
--select sum(C.ph1to1h2o_r * A.area)/sum(A.Area)\n\
from #aggarea A\n\
inner join mapunit M\n\
on A.id = M.mukey\n\
Inner Join component Co\n\
on Co.mukey = M.mukey\n\
Inner Join chorizon C\n\
on Co.cokey = C.coKey\n\
where A.id = M.mukey;\n\
--group by id;'
        body = f'<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:sdm="http://SDMDataAccess.nrcs.usda.gov/Tabular/SDMTabularService.asmx">\n\
<soap:Header/>\n\
<soap:Body>\n\
<sdm:RunQuery>\n\
<sdm:Query>{query}</sdm:Query>\n\
</sdm:RunQuery>\n\
</soap:Body>\n\
</soap:Envelope>'
        
        #response_xml = cls.session.post(f'{cls.root}', data=body, headers=cls.headers)
        #if not response_xml.status_code == 200:
        #    # print(xmltodict.parse(response_xml.content, process_namespaces=False))
        #    raise ValueError('USDA Soil Data Mart API call Error')
        #response_dict = xmltodict.parse(response_xml.content, process_namespaces=False)
        #return response_dict

        cls._parcel = parcel_name
        response_dict = UsdaApi._post_query(body)
        return response_dict

    @classmethod
    def get_component_coordinates(cls, parcel_coords, username=None, password=None):
        cls.headers['Content-Type'] = 'text/xml'
        vertex = parcel_coords
        query = f'-- Define a triangular AOI in WGS84\n\
        ~DeclareGeometry(@aoi)~\n\
        -- Parcel W1 of Foundries\n\
        select @aoi = geometry::STPolyFromText(\'polygon((\
        {vertex} \
        ))\', 4326) \n\
        -- Extract all intersected polygons\n\
        ~DeclareIdGeomTable(@intersectedPolygonGeometries)~\n\
        ~GetClippedMapunits(@aoi,polygon,geo,@intersectedPolygonGeometries)~\n\
        -- Convert geometries to geographies so we can get areas\n\
        ~DeclareIdGeogTable(@intersectedPolygonGeographies)~\n\
        ~GetGeogFromGeomWgs84(@intersectedPolygonGeometries,@intersectedPolygonGeographies)~\n\
        select *, geog.STArea() as area from @intersectedPolygonGeographies'
        body = f'<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:sdm="http://SDMDataAccess.nrcs.usda.gov/Tabular/SDMTabularService.asmx">\n\
        <soap:Header/>\n\
        <soap:Body>\n\
        <sdm:RunQuery>\n\
        <sdm:Query>{query}</sdm:Query>\n\
        </sdm:RunQuery>\n\
        </soap:Body>\n\
        </soap:Envelope>'
        response_xml = cls.session.post(f'{cls.root}', data=body, headers=cls.headers)
        if not response_xml.status_code == 200:
            raise ValueError('USDA Soil Data Mart API call Error')
        response_dict = xmltodict.parse(response_xml.content, process_namespaces=False)
        return response_dict

    @classmethod
    def _post_query(cls, body, attempts=3):
        logger = make_logger('usda_call')
        for attempt in range(attempts):
            try:
                response_xml = cls.session.post(
                    cls.root,
                    data=body,
                    headers=cls.headers,
                    timeout=(10, 90),
                )
                response_xml.raise_for_status()

                parsed = xmltodict.parse(
                    response_xml.content,
                    process_namespaces=False,
                )

                if "Fault" in str(parsed):
                    raise RuntimeError(f"USDA SOAP fault: {parsed}")

                return parsed
            
            except (requests.RequestException, RuntimeError) as e:
                logger.warning(f"Failed to fetch data for {cls._parcel} ({attempt+1}/{attempts}): {e}")
                if attempt == attempts - 1:
                    raise
                time.sleep(2 ** attempt)