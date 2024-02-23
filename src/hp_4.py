# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""
    res = [datetime.strptime(old_dt, "%Y-%m-%d").strftime('%d %b %Y') for old_dt in old_dates]
    return res


def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    if not isinstance(start, str) or not isinstance(n, int):
        
        raise TypeError()
    
    rng = []
    frmat = datetime.strptime(start, '%Y-%m-%d')
    for a in range(n):
        rng.append(frmat + timedelta(days=a))
    return rng

def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    date_range_len = date_range(start_date, len(values))
    zipped_list = list(zip(date_range_len, values))
    return zipped_list


def helper_static(infile):
    
    headSet = ("book_uid,isbn_13,patron_id,date_checkout,date_due,date_returned".
              split(','))
    
    with open(infile, 'r') as f:
        c = DictReader(f, fieldnames=headSet)
        all_rows = [row for row in c]

        all_rows.pop(0)
    
    return all_rows

def fees_report(infile, outfile):
    """Calculates late fees per patron id and writes a summary report to
    outfile."""
    
    dt_format = '%m/%d/%Y'
    rows = helper_static(infile)
    cv = defaultdict(float)

    for row in rows:
       
        patron = row['patron_id']
        due_on = datetime.strptime(row['date_due'], dt_format)
        returned_on = datetime.strptime(row['date_returned'], dt_format)
        late_days = (returned_on - due_on).days
        cv[patron]+= 0.25 * late_days if late_days > 0 else 0.0

    header = [
        {'patron_id': pn, 'late_fees': f'{fs:0.2f}'} for pn, fs in cv.items()
    ]

    with open(outfile, 'w') as outfile:
        final_out = DictWriter(outfile, ['patron_id', 'late_fees'])
        final_out.writeheader()
        final_out.writerows(header)


# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':
    
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    # BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
