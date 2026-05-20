-- Top 10 happiest countries by average 2015-2019
CREATE VIEW kpi_top10_happiest AS
SELECT 
    "Country",
    ROUND(AVG("Happiness_score")::numeric, 3) AS avg_score,
    ROUND(MIN("Happiness_score")::numeric, 3) AS min_score,
    ROUND(MAX("Happiness_score")::numeric, 3) AS max_score
FROM happiness_predictions
GROUP BY "Country"
ORDER BY avg_score DESC
LIMIT 10;

-- Best improvement and worst failling 
CREATE VIEW kpi_biggest_movers AS
SELECT
    "Country",
    MAX("Happiness_score") FILTER (WHERE year = 2015) AS score_2015,
    MAX("Happiness_score") FILTER (WHERE year = 2019) AS score_2019,
    ROUND((MAX("Happiness_score") FILTER (WHERE year = 2019) 
        - MAX("Happiness_score") FILTER (WHERE year = 2015))::numeric, 3) AS delta
FROM happiness_predictions
WHERE year IN (2015, 2019)
GROUP BY "Country"
HAVING MAX("Happiness_score") FILTER (WHERE year = 2015) IS NOT NULL
    AND MAX("Happiness_score") FILTER (WHERE year = 2019) IS NOT NULL
ORDER BY delta DESC;


-- Correlation between each fact with Hapinness score by year 
CREATE VIEW kpi_factor_correlation AS
SELECT
    year,
    ROUND(CORR("Economy_(GDP_per_Capita)", "Happiness_score")::numeric, 3) AS corr_gdp,
    ROUND(CORR("Family", "Happiness_score")::numeric, 3)                    AS corr_family,
    ROUND(CORR("Health_(Life_Expectancy)", "Happiness_score")::numeric, 3)  AS corr_health,
    ROUND(CORR("Freedom", "Happiness_score")::numeric, 3)                   AS corr"freedom",
    ROUND(CORR("Trust_(Government_Corruption)", "Happiness_score")::numeric, 3) AS corr_trust,
    ROUND(CORR("Generosity", "Happiness_score")::numeric, 3)                AS corr_generosity
FROM happiness_predictions
GROUP BY year
ORDER BY year;

-- Volatility per "Country" (which are the more unstable countries)
CREATE VIEW kpi_country_volatility AS
SELECT
    "Country",
    ROUND(STDDEV("Happiness_score")::numeric, 4) AS score_stddev,
    COUNT(year) AS years_present
FROM happiness_predictions
GROUP BY "Country"
HAVING COUNT(year) >= 3   -- only those countries with enough data
ORDER BY score_stddev DESC;


-- Dominant factor per "Country" 
CREATE VIEW kpi_dominant_factor AS
SELECT
    "Country",
    ROUND(AVG("Economy_(GDP_per_Capita)")::numeric, 3)      AS avg_gdp,
    ROUND(AVG("Family")::numeric, 3)                        AS avg_family,
    ROUND(AVG("Health_(Life_Expectancy)")::numeric, 3)                        AS avg_health,
    ROUND(AVG("Freedom")::numeric, 3)                       AS avg_freedom,
    ROUND(AVG("Trust_(Government_Corruption)")::numeric, 3) AS avg_trust,
    ROUND(AVG("Generosity")::numeric, 3)                    AS avg_generosity,
    GREATEST(
        AVG("Economy_(GDP_per_Capita)"),
        AVG("Family"),
        AVG("Health_(Life_Expectancy)"),
        AVG("Freedom"),
        AVG("Trust_(Government_Corruption)"),
        AVG("Generosity")
    ) AS max_factor_value
FROM happiness_predictions
GROUP BY "Country";

-- Global evolution year by year

CREATE VIEW kpi_global_trend AS
SELECT
    year,
    ROUND(AVG("Happiness_score")::numeric, 3)  AS global_avg_score,
    ROUND(AVG("Economy_(GDP_per_Capita)")::numeric, 3) AS global_avg_gdp,
    ROUND(AVG("Family")::numeric, 3)           AS global_avg_family,
    ROUND(AVG("Freedom")::numeric, 3)          AS global_avg_freedom,
    COUNT(DISTINCT "Country")                  AS countries_reported
FROM happiness_predictions
GROUP BY year
ORDER BY year;