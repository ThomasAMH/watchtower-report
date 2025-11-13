### Data Reading
    Confirm: Clear program data from ...?
    Clear program data.
    Create meta_data.json
        - Has data creation time, statistics, etc.
    Iterate through all input_data directories, and based on the directory name, and read all necessary information into program data files:
        - Each one is named after the input file, but contains only vital information as specified in headers.json
        - Map everything based on config.json
    Move all read reports into read data in a directory based on the date (if already exists, override)
    Use pandas for speed and simplicity

## UI
    - Runs in the terminal with simple user interface (1, 2, 3, all, etc.)
    - Takes options (?)
    - Scripts executable individually

## Reports
    - Each report gets its own directory. When generated, overwrite previous reports.
    - Each report has its own config directory with report elements in json files specifying which headers should be included
    - Report logic is contained in the code itself, but is clearly outlined
    - Variables are included in the report's config file

### DTX to WH Report
    1. Read in all DTX data from before a specified offset date (see config)
    2. Get array of all orders in status 3
    3. Read in all order numbers from on hold, backorder, and watchtower
    4. Categorize all status 3 orders based on status
    5. Output DTX data as configured, indicating what is needed
    6. Indicate which orders are in status 3 but are not yet shipped (between a date period)
    7. Write report.json with the report statistics


### Imported Orders Breakdown
    1. Read in all orders from on-hold, backorder, and unshipped...?
    2. Summarize On Holds with sub-module by day
    3. Summarize imported, ready to ship, by day
    4. Show overdue orders that are not on hold according to config
    5. Show SKU breakdown for overdue orders
    6. Write report.json with the report statistics

### Watchtower Report
    1. Read in all shipped orders,
    2. Flag those that are OVERDUE (transit time + tolorance) that do NOT have a replacement
    3. Gather statistics for each country over period showing ship dates, avg transit time, carriers.
    4. Flag those with percentages / orders over the configured limit (5%, but at least 10, for example)
    5. End result should be: How are orders making it to their destinations around Europe, and for those that aren't, do we know?

    Table of orders delivered by day, table of vital statistics over period (transit time)
    Know what wrong looks like and flag it (Danger Table) based on pre-defined statistics

    Key statistics
    % orders delayed
    % orders not delivered
    ^ Calculated for each country and stored


### Spyglass Report
    Generated provided country, shipping config, etc, and provides day-by-day breakdown of the statistics already calculated in the report.json


### Export Raw data
    - Dump all program data json files into csv's based on the headers config

Do Later:
Move read data to a different directory
