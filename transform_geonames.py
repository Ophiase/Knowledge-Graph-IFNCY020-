import os
import pandas as pd
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from typing import Dict, Tuple

###################################################################################

DATA_FOLDER = os.path.join("data", "geonames")
OUTPUT_FILE = os.path.join("data", "geonames_knowledge_graph.rdf")
VERBOSE = True
LINE_LIMIT = 10000

###################################################################################


def create_graph() -> Tuple[Graph, Namespace]:
    g = Graph()
    EX = Namespace("http://example.org/geonames/")
    g.bind("ex", EX)
    return g, EX


def add_triples(g: Graph, df: pd.DataFrame, subject_class: URIRef, subject_prefix: str, properties: Dict[URIRef, str], id_column: str) -> None:
    for _, row in df.iterrows():
        subject = URIRef(f"{subject_prefix}{row[id_column]}")
        g.add((subject, RDF.type, subject_class))
        for prop, col in properties.items():
            if pd.notna(row[col]):
                g.add((subject, prop, Literal(row[col])))


def process_admin1_codes(g: Graph, EX: Namespace, df: pd.DataFrame) -> None:
    add_triples(g, df, EX.Admin1Code, EX.admin1Code, {
        EX.code: "code",
        EX.name: "name",
        EX.name_ascii: "name_ascii",
        EX.geonameid: "geonameid"
    }, "code")


def process_admin2_codes(g: Graph, EX: Namespace, df: pd.DataFrame) -> None:
    add_triples(g, df, EX.Admin2Code, EX.admin2Code, {
        EX.code: "code",
        EX.name: "name",
        EX.asciiname: "asciiname",
        EX.geonameid: "geonameid"
    }, "code")


def process_admin5_codes(g: Graph, EX: Namespace, df: pd.DataFrame) -> None:
    add_triples(g, df, EX.Admin5Code, EX.admin5Code, {
        EX.geonameid: "geonameid",
        EX.adm5code: "adm5code"
    }, "geonameid")


def process_alternate_names(g: Graph, EX: Namespace, df: pd.DataFrame) -> None:
    add_triples(g, df, EX.AlternateName, EX.alternateName, {
        EX.alternateNameId: "alternateNameId",
        EX.geonameid: "geonameid",
        EX.isolanguage: "isolanguage",
        EX.alternate_name: "alternate_name"
    }, "alternateNameId")


def process_cities(g: Graph, EX: Namespace, df: pd.DataFrame) -> None:
    add_triples(g, df, EX.City, EX.city, {
        EX.geonameid: "geonameid",
        EX.name: "name",
        EX.asciiname: "asciiname",
        EX.alternatenames: "alternatenames",
        EX.latitude: "latitude",
        EX.longitude: "longitude",
        EX.feature_class: "feature_class",
        EX.feature_code: "feature_code",
        EX.country_code: "country_code",
        EX.cc2: "cc2",
        EX.admin1_code: "admin1_code",
        EX.admin2_code: "admin2_code",
        EX.admin3_code: "admin3_code",
        EX.admin4_code: "admin4_code",
        EX.population: "population",
        EX.elevation: "elevation",
        EX.dem: "dem",
        EX.timezone: "timezone",
        EX.modification_date: "modification_date"
    }, "geonameid")


def process_country_info(g: Graph, EX: Namespace, df: pd.DataFrame) -> None:
    add_triples(g, df, EX.CountryInfo, EX.countryInfo, {
        EX.iso: "ISO",
        EX.iso3: "ISO3",
        EX.iso_numeric: "ISO-Numeric",
        EX.fips: "fips",
        EX.country: "Country",
        EX.capital: "Capital",
        EX.area_in_sq_km: "Area(in sq km)",
        EX.population: "Population",
        EX.continent: "Continent",
        EX.tld: "tld",
        EX.currency_code: "CurrencyCode",
        EX.currency_name: "CurrencyName",
        EX.phone: "Phone",
        EX.postal_code_format: "Postal Code Format",
        # EX.postal_code_regex: "Postal Code Regex",
        # EX.languages: "Languages",
        # EX.geonameid: "geonameid",
        # EX.neighbours: "neighbours",
        # EX.equivalent_fips_code: "EquivalentFipsCode"
    }, "ISO")


def process_feature_codes(g: Graph, EX: Namespace, df: pd.DataFrame) -> None:
    add_triples(g, df, EX.FeatureCode, EX.featureCode, {
        EX.code: "code",
        EX.name: "name",
        EX.description: "description"
    }, "code")


def process_hierarchy(g: Graph, EX: Namespace, df: pd.DataFrame) -> None:
    add_triples(g, df, EX.Hierarchy, EX.hierarchy, {
        EX.parentId: "parentId",
        EX.childId: "childId",
        EX.type: "type"
    }, "parentId")


def process_iso_language_codes(g: Graph, EX: Namespace, df: pd.DataFrame) -> None:
    df.columns = [col.replace(" ", "_") for col in df.columns]
    add_triples(g, df, EX.ISOLanguageCode, EX.isoLanguageCode, {
        EX.iso_639_3: "ISO_639_3",
        EX.iso_639_2: "ISO_639_2",
        EX.iso_639_1: "ISO_639_1",
        EX.language_name: "Language_Name"
    }, "ISO_639_3")


def process_time_zones(g: Graph, EX: Namespace, df: pd.DataFrame) -> None:
    add_triples(g, df, EX.TimeZone, EX.timeZone, {
        EX.country_code: "CountryCode",
        EX.timezone_id: "TimeZoneId",
        EX.gmt_offset: "GMT_offset_1_Jan_2025",
        EX.dst_offset: "DST_offset_1_Jul_2025",
        EX.raw_offset: "rawOffset_independant_of_DST"
    }, "CountryCode")

###################################################################################


def process_file(g: Graph, EX: Namespace, file_name: str, file_path: str) -> None:
    if VERBOSE:
        print(f"Processing {file_name}...")

    file_columns = {
        "admin1CodesASCII.txt": ["code", "name", "name_ascii", "geonameid"],
        "admin2Codes.txt": ["code", "name", "asciiname", "geonameid"],
        "adminCode5.txt": ["geonameid", "adm5code"],
        "alternateNamesV2.txt": ["alternateNameId", "geonameid", "isolanguage", "alternate_name", "isPreferredName", "isShortName", "isColloquial", "isHistoric", "from", "to"],
        "cities500.txt": ["geonameid", "name", "asciiname", "alternatenames", "latitude", "longitude", "feature_class", "feature_code", "country_code", "cc2", "admin1_code", "admin2_code", "admin3_code", "admin4_code", "population", "elevation", "dem", "timezone", "modification_date"],
        "cities1000.txt": ["geonameid", "name", "asciiname", "alternatenames", "latitude", "longitude", "feature_class", "feature_code", "country_code", "cc2", "admin1_code", "admin2_code", "admin3_code", "admin4_code", "population", "elevation", "dem", "timezone", "modification_date"],
        "cities5000.txt": ["geonameid", "name", "asciiname", "alternatenames", "latitude", "longitude", "feature_class", "feature_code", "country_code", "cc2", "admin1_code", "admin2_code", "admin3_code", "admin4_code", "population", "elevation", "dem", "timezone", "modification_date"],
        "cities15000.txt": ["geonameid", "name", "asciiname", "alternatenames", "latitude", "longitude", "feature_class", "feature_code", "country_code", "cc2", "admin1_code", "admin2_code", "admin3_code", "admin4_code", "population", "elevation", "dem", "timezone", "modification_date"],
        "countryInfo.txt": ["ISO", "ISO3", "ISO-Numeric", "fips", "Country", "Capital", "Area(in sq km)", "Population", "Continent", "tld", "CurrencyCode", "CurrencyName", "Phone", "Postal Code Format"],# "Postal Code Regex", "Languages", "geonameid", "neighbours", "EquivalentFipsCode"],
        "featureCodes_en.txt": ["code", "name", "description"],
        "hierarchy.txt": ["parentId", "childId", "type"],
        "iso-languagecodes.txt": ["ISO_639_3", "ISO_639_2", "ISO_639_1", "Language_Name"],
        "timeZones.txt": ["CountryCode", "TimeZoneId", "GMT_offset_1_Jan_2025", "DST_offset_1_Jul_2025", "rawOffset_independant_of_DST"]
    }

    if file_name in file_columns:
        df = pd.read_csv(file_path, delimiter='\t', nrows=LINE_LIMIT, header=None, comment='#', on_bad_lines='skip')
        df.columns = file_columns[file_name]
        match file_name:
            case "admin1CodesASCII.txt":
                process_admin1_codes(g, EX, df)
            case "admin2Codes.txt":
                process_admin2_codes(g, EX, df)
            case "adminCode5.txt":
                process_admin5_codes(g, EX, df)
            case "alternateNamesV2.txt":
                process_alternate_names(g, EX, df)
            case "cities500.txt" | "cities1000.txt" | "cities5000.txt" | "cities15000.txt":
                process_cities(g, EX, df)
            case "countryInfo.txt":
                process_country_info(g, EX, df)
            case "featureCodes_en.txt":
                process_feature_codes(g, EX, df)
            case "hierarchy.txt":
                process_hierarchy(g, EX, df)
            case "iso-languagecodes.txt":
                df = df.drop(0)
                process_iso_language_codes(g, EX, df)
            case "timeZones.txt":
                process_time_zones(g, EX, df)
    else:
        if VERBOSE:
            print(f"File {file_name} not recognized, skipping.")

###################################################################################


def main():
    g, EX = create_graph()
    for file_name in os.listdir(DATA_FOLDER):
        file_path = os.path.join(DATA_FOLDER, file_name)
        process_file(g, EX, file_name, file_path)
    print("serialize...")
    g.serialize(destination=OUTPUT_FILE, format='xml')
    print("done")


if __name__ == "__main__":
    main()