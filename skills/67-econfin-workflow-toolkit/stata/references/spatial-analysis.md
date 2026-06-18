# Spatial Analysis in Stata

## Contents

- [Spatial Data Structures](#spatial-data-structures)
- [Creating and Managing Shapefiles](#creating-and-managing-shapefiles)
- [Spatial Weights Matrices](#spatial-weights-matrices)
- [Spatial Autocorrelation](#spatial-autocorrelation)
- [Spatial Regression Models](#spatial-regression-models)
- [The spregress Command](#the-spregress-command)
- [Geographic Visualization](#geographic-visualization)
- [Distance Calculations](#distance-calculations)
- [Spatial Panel Data](#spatial-panel-data)
- [Geospatial File Formats](#geospatial-file-formats)
- [Practical Examples](#practical-examples)

---

## Spatial Data Structures

Stata organizes spatial data into two linked datasets:

1. **Attribute Data** -- regular .dta with variables for analysis
2. **Spatial Data** -- coordinate/shape information (_shp.dta file)

### The spset Command

Links attribute data to spatial coordinate data.

```stata
* Set spatial structure with linked shapefile
spset county_id using county_shp.dta

* Point data from coordinates
spset id, coord(latitude longitude) modify

* Check current spatial settings
spset
```

---

## Creating and Managing Shapefiles

### Loading Shapefiles

```stata
* Method 1: spshape2dta (preferred)
spshape2dta county_boundaries, replace saving(county_sp)
* Creates: county_sp.dta (attributes) + county_sp_shp.dta (coordinates)

use county_sp, clear
spset

* Method 2: shp2dta (older)
shp2dta using county_boundaries, ///
    database(county_data) coordinates(county_coords) genid(id) replace

use county_data, clear
spset id using county_coords
```

### Creating Point Data from Coordinates

```stata
clear
input id latitude longitude population
1 40.7128 -74.0060 8336817
2 34.0522 -118.2437 3979576
end

spset id, coord(latitude longitude) modify
save city_points, replace
```

### Merging Attribute Data with Shapefiles

```stata
use county_sp, clear
merge 1:1 county_id using socioeconomic_data
keep if _merge == 3
drop _merge
spset county_id
```

---

## Spatial Weights Matrices

Define neighborhood structure and strength of spatial relationships. Element w[i,j] indicates the relationship between observations i and j. Diagonal is always zero.

### Contiguity-Based Weights

```stata
* Rook contiguity (shared border only)
spmatrix create contiguity W, rook normalize(row)

* Queen contiguity (shared border or vertex)
spmatrix create contiguity W, queen normalize(row)

* Summarize the weights matrix
spmatrix summarize W
spmatrix summarize W, id(1)    // neighbors for observation 1
```

### Distance-Based Weights

```stata
* Inverse distance (weight decreases with distance)
spmatrix create idistance W_dist, normalize(row) vdistance(euclid)

* Inverse distance squared (faster decay)
spmatrix create idistance W_dist2, normalize(row) vdistance(euclid) power(2)

* Fixed distance band (neighbors within 50 km)
spmatrix create idistance W_band, band(0 50) normalize(row)

* K-nearest neighbors (5 closest)
spmatrix create idistance W_knn, knn(5) normalize(row)
```

### Custom Weights in Mata

```stata
mata:
    W_custom = J(100, 100, 0)
    for (i=1; i<=100; i++) {
        for (j=1; j<=100; j++) {
            if (i != j & abs(i-j) <= 5) W_custom[i,j] = 1/(abs(i-j))
        }
    }
    st_matrix("W", W_custom)
end

spmatrix spfrommata W_custom = W, normalize(row)
```

### Normalization Options

```stata
spmatrix create contiguity W_raw, queen                    // no normalization
spmatrix create contiguity W_norm, queen normalize(row)     // rows sum to 1
spmatrix create contiguity W_spec, queen normalize(spectral) // spectral norm
```

### Inspecting Weights in Mata

```stata
spmatrix matafromsp W_cont W_mata
mata: W_mata[1..10, 1..10]
```

---

## Spatial Autocorrelation

### Moran's I

Global measure of spatial autocorrelation. Range: -1 (dispersion) to +1 (clustering). I=0 means random spatial pattern.

```stata
spmatrix create contiguity W, queen normalize(row)

* Test single variable
estat moran unemployment, weight(W)

* Test multiple variables
estat moran unemployment income education, weight(W)

* Permutation-based inference (more robust)
estat moran income, weight(W) permutations(999)
```

### Geary's C

Alternative to Moran's I based on differences rather than covariance. C<1 = positive autocorrelation, C=1 = none, C>1 = negative.

```stata
estat geary unemployment, weight(W)
```

### Local Indicators of Spatial Association (LISA)

Identifies spatial clusters and outliers at the local level.

```stata
spgenerate lisa_income = lisa(income), weight(W)

* Classify: High-High, Low-Low, High-Low, Low-High
generate cluster_type = ""
replace cluster_type = "High-High" if lisa_income > 0 & income > r(mean)
replace cluster_type = "Low-Low" if lisa_income > 0 & income < r(mean)
replace cluster_type = "High-Low" if lisa_income < 0 & income > r(mean)
replace cluster_type = "Low-High" if lisa_income < 0 & income < r(mean)
```

---

## Spatial Regression Models

### Model Summary Table

| Model | Specification | When to Use | Stata Command |
|-------|--------------|-------------|---------------|
| **OLS** | y = Xb + e | No spatial dependence | `regress` |
| **SAR** | y = rWy + Xb + e | Spillovers in outcome | `spregress, dvarlag(W)` |
| **SEM** | y = Xb + u; u = lWu + e | Spatial error correlation | `spregress, errorlag(W)` |
| **SDM** | y = rWy + Xb + WXt + e | Spillovers in X and y | `spregress, dvarlag(W) ivarlag(W:)` |
| **SLX** | y = Xb + WXt + e | Spillovers only in X | `spregress, ivarlag(W:)` |
| **SAC** | y = rWy + Xb + u; u = lWu + e | Both lag and error | `spregress, dvarlag(W) errorlag(W)` |

### When to Use Which

- **SAR (Spatial Lag):** Theory suggests spatial spillovers in outcome (e.g., regional growth, disease spread)
- **SEM (Spatial Error):** Spatial pattern in residuals from omitted variables; main interest is in beta, not spatial process
- **SDM (Spatial Durbin):** Both own and neighbors' characteristics matter; theory unclear about mechanism; can test down to SAR or SEM

### Lagrange Multiplier Tests for Model Selection

```stata
regress income education unemployment poverty

* LM tests
estat lmsar, weight(W)    // test for spatial lag
estat lmse, weight(W)     // test for spatial error

* Robust LM tests
estat rlmsar, weight(W)
estat rlmse, weight(W)
```

**Decision rule:**
1. Both insignificant -> OLS
2. Only LM-Lag significant -> SAR
3. Only LM-Error significant -> SEM
4. Both significant -> use robust tests or SDM

---

## The spregress Command

### Syntax

```stata
spregress depvar indepvars [if] [in] [, options]
```

### Key Options

**Spatial structure:**
- `dvarlag(spmatrix)` -- spatial lag of dependent variable (SAR)
- `errorlag(spmatrix)` -- spatial lag of errors (SEM)
- `ivarlag(spmatrix: varlist)` -- spatial lag of independent variables (SLX)

**Estimation method:**
- `ml` -- maximum likelihood (default)
- `gs2sls` -- generalized spatial 2SLS

**Standard errors:**
- `vce(oim)` -- observed information matrix (default)
- `vce(robust)` -- heteroskedasticity-robust
- `vce(cluster clustvar)` -- cluster-robust

### All Model Specifications

```stata
* SAR
spregress y x1 x2 x3, ml dvarlag(W)

* SEM
spregress y x1 x2 x3, ml errorlag(W)

* SDM
spregress y x1 x2 x3, ml dvarlag(W) ivarlag(W: x1 x2 x3)

* SAC/SARAR (can use different W matrices)
spregress y x1 x2 x3, ml dvarlag(W1) errorlag(W2)

* SLX
spregress y x1 x2 x3, ml ivarlag(W: x1 x2 x3)
```

### Direct, Indirect, and Total Effects

In spatial lag models, a change in X produces feedback effects through the spatial multiplier, so the impact is not simply beta.

```stata
spregress income education unemployment, ml dvarlag(W)
estat impact education unemployment

* Direct effect: impact on unit i from change in i's own X
* Indirect effect: spillover from neighbors' X changes
* Total effect: Direct + Indirect
```

### Post-Estimation

```stata
* Impact measures (for models with spatial lag)
estat impact [varlist]

* Information criteria
estat ic

* Predictions
predict yhat, xb
predict resid, residuals

* Marginal effects
margins, dydx(*)

* Test spatial parameters
test _b[/rho] = 0       // spatial lag
test _b[/lambda] = 0    // spatial error
```

### Comprehensive Model Comparison Example

```stata
webuse "texas_counties", clear
spset county_id
spmatrix create contiguity W, queen normalize(row)

* OLS baseline
regress income education unemployment poverty
estimates store m1_ols
predict resid_ols, residuals
estat moran resid_ols, weight(W)

* SAR
spregress income education unemployment poverty, ml dvarlag(W) vce(robust)
estimates store m2_sar
estat impact

* SEM
spregress income education unemployment poverty, ml errorlag(W) vce(robust)
estimates store m3_sem

* SDM
spregress income education unemployment poverty, ///
    ml dvarlag(W) ivarlag(W: education unemployment poverty) vce(robust)
estimates store m4_sdm
estat impact

* Compare all models
estimates table m1_ols m2_sar m3_sem m4_sdm, ///
    star stats(N r2 ll aic bic) b(%9.3f) se

* LR test nested models
lrtest m2_sar m4_sdm
```

---

## Geographic Visualization

### spmap (user-written)

```stata
ssc install spmap
ssc install shp2dta
```

### Choropleth Maps

```stata
* Quantile classification
spmap income using county_shp, id(county_id) ///
    clmethod(quantile) clnumber(5) fcolor(Blues)

* Custom breaks
spmap income using county_shp, id(county_id) ///
    clmethod(custom) clbreaks(0 20000 40000 60000 80000 100000) ///
    legend(title("Income ($)"))
```

### Classification Methods

```stata
spmap y using shp, id(_ID) clmethod(quantile) clnumber(5)   // equal counts per class
spmap y using shp, id(_ID) clmethod(eqint) clnumber(5)      // equal intervals
spmap y using shp, id(_ID) clmethod(natural) clnumber(5)    // Jenks natural breaks
spmap y using shp, id(_ID) clmethod(stdev)                  // standard deviations
spmap y using shp, id(_ID) clmethod(custom) clbreaks(0 10 20 30 40 50)
```

### Color Schemes

```stata
spmap y using shp, id(_ID) fcolor(Blues)    // sequential
spmap y using shp, id(_ID) fcolor(RdBu)     // diverging
spmap y using shp, id(_ID) fcolor(Set1)     // categorical
spmap y using shp, id(_ID) fcolor(Grays)    // grayscale
```

### Small Multiple Maps

```stata
foreach var in income education unemployment {
    spmap `var' using county_shp, id(county_id) ///
        clmethod(quantile) clnumber(5) ///
        title("`var'") saving(`var'_map, replace)
}
graph combine income_map.gph education_map.gph unemployment_map.gph, rows(1)
```

### Point Overlays and Labels

```stata
* Points on a polygon map
spmap using county_shp, id(county_id) ///
    point(data(city_points) xcoord(longitude) ycoord(latitude) ///
          by(population) fcolor(red) size(*0.5))

* Labels
spmap income using county_shp, id(county_id) ///
    label(data(county_sp) xcoord(_CX) ycoord(_CY) ///
          label(county_name) size(*0.5))
```

---

## Distance Calculations

### Using spmatrix for Distance

```stata
* Inverse distance
spmatrix create idistance W_dist, vdistance(euclid) normalize(row)

* Distance band (neighbors within 100 km)
spmatrix create idistance W_band, band(0 100) vdistance(euclid) normalize(row)

* K-nearest neighbors
spmatrix create idistance W_knn, knn(5) vdistance(euclid) normalize(row)
```

### Geodetic vs. Planar Distance

```stata
* For lat/long: use geodetic distance (kilometers)
spset county_id, coord(latitude longitude) coordsys(latlong)
spmatrix create idistance W_geo, vdistance(geodetic) dfunction(dhaversine) normalize(row)

* For projected coordinates (meters): use Euclidean
spset county_id, coord(x_meters y_meters) coordsys(planar)
spmatrix create idistance W_planar, vdistance(euclid) normalize(row)
```

### Distance Decay Options

```stata
* Inverse distance
spmatrix create idistance W_inv, vdistance(euclid) power(1) normalize(row)

* Inverse distance squared (faster decay)
spmatrix create idistance W_inv2, vdistance(euclid) power(2) normalize(row)
```

### Custom Exponential Decay in Mata

```stata
mata:
    D = st_matrix("dist_matrix")
    alpha = 0.1
    W_exp = exp(-alpha * D)
    _diag(W_exp, 0)
    row_sums = rowsum(W_exp)
    for (i=1; i<=rows(W_exp); i++) {
        if (row_sums[i] > 0) W_exp[i,.] = W_exp[i,.] / row_sums[i]
    }
    st_matrix("W_exp", W_exp)
end
spmatrix spfrommata W_exp = W_exp
```

### Haversine Distance in Mata

```stata
mata:
    function haversine(lat1, lon1, lat2, lon2) {
        R = 6371  // Earth radius in km
        lat1_rad = lat1 * pi() / 180
        lat2_rad = lat2 * pi() / 180
        dLat = (lat2 - lat1) * pi() / 180
        dLon = (lon2 - lon1) * pi() / 180
        a = sin(dLat/2)^2 + cos(lat1_rad) * cos(lat2_rad) * sin(dLon/2)^2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        return(R * c)
    }
end
```

---

## Spatial Panel Data

Combines spatial (N units) and temporal (T periods) dimensions.

### Setup

```stata
use county_panel, clear
xtset county_id year           // panel structure
spset county_id                 // spatial structure
spmatrix create contiguity W, queen normalize(row)
```

### spxtregress Models

```stata
* Spatial lag with unit fixed effects
spxtregress income education unemployment, fe dvarlag(W) type(fixed)

* Add time fixed effects
spxtregress income education unemployment i.year, fe dvarlag(W) type(fixed)

* Random effects spatial lag
spxtregress income education unemployment, re dvarlag(W) type(random)

* Spatial error with fixed effects
spxtregress income education unemployment, fe errorlag(W) type(fixed)

* Spatial Durbin panel
spxtregress income education unemployment, ///
    fe dvarlag(W) ivarlag(W: education unemployment) type(fixed)
```

### Complete Spatial Panel Example

```stata
use county_panel, clear
xtset county_id year
spset county_id
spmatrix create contiguity W, queen normalize(row)

* Standard panel FE (baseline)
xtreg income education unemployment poverty, fe
estimates store panel_fe

* Spatial lag FE
spxtregress income education unemployment poverty, fe dvarlag(W) type(fixed)
estimates store sp_lag_fe

* Spatial error FE
spxtregress income education unemployment poverty, fe errorlag(W) type(fixed)
estimates store sp_err_fe

* Spatial Durbin FE
spxtregress income education unemployment poverty, ///
    fe dvarlag(W) ivarlag(W: education unemployment poverty) type(fixed)
estimates store sp_dur_fe

* With time FE
spxtregress income education unemployment poverty i.year, ///
    fe dvarlag(W) type(fixed)
estimates store sp_lag_fe_time
testparm i.year

* Compare
estimates table panel_fe sp_lag_fe sp_err_fe sp_dur_fe, ///
    star stats(N ll aic bic) b(%9.3f)

* Spillover effects
estimates restore sp_lag_fe
estat impact education unemployment poverty
```

### Spatial Panel Diagnostics

```stata
predict resid, residuals

* Test residuals by year
forvalues t = 1/10 {
    preserve
    keep if year == `t'
    estat moran resid, weight(W)
    restore
}
```

---

## Geospatial File Formats

### Shapefile (.shp)

Components: `.shp` (geometry), `.dbf` (attributes), `.shx` (index), `.prj` (projection)

```stata
spshape2dta county_boundaries, replace saving(county_sp)
* Creates: county_sp.dta + county_sp_shp.dta

use county_sp, clear
describe
use county_sp_shp, clear
list _ID _X _Y in 1/10
```

### GeoJSON / KML

Convert externally first, then import:
```stata
* Use ogr2ogr (GDAL) in terminal:
* ogr2ogr -f "ESRI Shapefile" output.shp input.geojson
* Then: spshape2dta output, replace saving(geo_data)
```

### CSV with Coordinates (Point Data)

```stata
import delimited "locations.csv", clear
spset id, coord(latitude longitude) coordsys(latlong)
spmatrix create idistance W, knn(5) normalize(row)
spregress value predictor1 predictor2, ml dvarlag(W)
```

### Coordinate Systems

```stata
* Latitude/Longitude (WGS84)
spset county_id, coord(lat lon) coordsys(latlong)

* Projected coordinates (meters)
spset county_id, coord(x_meters y_meters) coordsys(planar)
```

---

## Practical Examples

### Example 1: County Income Analysis (Full Workflow)

```stata
webuse "texas_counties", clear
spset county_id
spmatrix create contiguity W, queen normalize(row)

* Test for spatial autocorrelation
estat moran income, weight(W)

* Visualize
spmap income using texas_counties_shp, id(county_id) ///
    clmethod(quantile) clnumber(5) fcolor(YlOrRd) ///
    legend(title("Median Income"))

* OLS baseline + residual test
regress income education unemployment poverty
estimates store ols
predict resid_ols, residuals
estat moran resid_ols, weight(W)

* Spatial lag model
spregress income education unemployment poverty, ml dvarlag(W) vce(robust)
estimates store sar
estat impact education unemployment poverty

* Compare OLS, SAR, SEM, SDM
spregress income education unemployment poverty, ml errorlag(W) vce(robust)
estimates store sem

spregress income education unemployment poverty, ///
    ml dvarlag(W) ivarlag(W: education unemployment poverty) vce(robust)
estimates store sdm

estimates table ols sar sem sdm, star stats(N r2 ll aic bic) b(%9.3f) se

* LISA clusters
spgenerate lisa_income = lisa(income), weight(W)
generate cluster_type = 1 if lisa_income > 0 & income > r(mean)
replace cluster_type = 2 if lisa_income > 0 & income < r(mean)
replace cluster_type = 3 if lisa_income < 0 & income > r(mean)
replace cluster_type = 4 if lisa_income < 0 & income < r(mean)
label define cluster_lbl 1 "High-High" 2 "Low-Low" 3 "High-Low" 4 "Low-High"
label values cluster_type cluster_lbl

spmap cluster_type using texas_counties_shp, id(county_id) ///
    clmethod(unique) fcolor(red blue yellow green) ///
    legend(title("Spatial Clusters"))
```

### Example 2: Housing Prices with Distance Decay

```stata
spset id, coord(lat lon) coordsys(latlong)

* Inverse distance weights (geodetic)
spmatrix create idistance W_inv2, ///
    vdistance(geodetic) dfunction(dhaversine) power(2) normalize(row)

* OLS vs spatial lag
regress price sqft bedrooms distance_cbd
estimates store ols

spregress price sqft bedrooms distance_cbd, ml dvarlag(W_inv2)
estimates store sar_inv2

estimates table ols sar_inv2, star stats(N r2 ll aic)
estat impact sqft bedrooms distance_cbd
```

---

## Best Practices

### Choosing Weights Matrices

- **Contiguity:** administrative boundaries with clear neighbors
- **Distance:** point data or when distance matters theoretically
- **K-nearest neighbors:** ensures uniform neighbor count
- **Distance bands:** specific geographic range of influence
- Always test multiple specifications and compare AIC

```stata
foreach w in W1 W2 W3 {
    quietly spregress y x1 x2, ml dvarlag(`w')
    estat ic
}
```

### Model Selection Workflow

1. Estimate OLS
2. Test residuals: `estat moran resid, weight(W)`
3. If significant, estimate SAR, SEM, SDM
4. Compare with `estat ic` (AIC/BIC)
5. For lag models, always report `estat impact`

### Robustness Checks

```stata
* Vary number of neighbors
foreach k in 4 5 6 7 8 {
    spmatrix create idistance W`k', knn(`k') normalize(row)
    quietly spregress y x1 x2, ml dvarlag(W`k')
    estimates store model_k`k'
}
estimates table model_k*, star stats(N ll aic)
```

### Common Pitfalls

- Forgetting to row-standardize weights
- Mixing coordinate systems (lat/lon vs. projected)
- Reporting only beta without direct/indirect effects for SAR models
- Not testing OLS residuals for spatial autocorrelation before using spatial models
- Missing data creates holes in spatial structure -- check with `misstable summarize`

### Reporting Spatial Results

Always include:
- Spatial parameter (rho or lambda) with SE
- Direct, indirect, total effects (for lag models)
- Moran's I test results
- Weights matrix specification + average neighbors
- AIC/BIC for model comparison

### User-Written Packages

```stata
ssc install spmap       // choropleth maps
ssc install shp2dta     // shapefile conversion
ssc install spwmatrix   // additional weights options
ssc install splagvar    // spatial lag variables
```
