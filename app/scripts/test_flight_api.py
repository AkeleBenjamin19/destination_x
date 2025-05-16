#!/usr/bin/env python
# app/scripts/fetch_and_save_flights.py

import os
import sys
import asyncio
from pathlib import Path
from dotenv import load_dotenv

# 1) Ensure project root is on Python path
PROJECT_ROOT = Path(__file__).parents[2]  # two levels up from this script
sys.path.insert(0, str(PROJECT_ROOT))

# 2) Load environment variables (Amadeus creds, DATABASE_URL, etc.)
load_dotenv(PROJECT_ROOT / ".env")

from app import create_app
from app.services.flight_api_service import FlightAPIService


def main():
    # Create Flask app context
    app = create_app()
    with app.app_context():
        svc = FlightAPIService()
        
        # Sample data: Miami (MIA) -> London Heathrow (LHR)
        origin = 'MIA'
        destination = 'LAX'
        departure = '2025-07-01'
        return_date = '2025-07-10'
        adults = 1

        print(f"Fetching best flight from {origin} to {destination} on {departure} returning {return_date} for {adults} adult(s)")
        # Run the async method and wait for result
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        entries = loop.run_until_complete(
            svc.get_price_entries(origin, destination, departure, return_date, adults)
        )
        loop.close()

        if not entries:
            print("No flight entries found.")
            return

        for entry in entries:
            print("-- Flight Offer --")
            print(f"Origin City ID:      {entry['origin_city_id']}")
            print(f"Destination City ID: {entry['destination_city_id']}")
            print(f"Departure Date:      {entry['departure_date']}")
            print(f"Return Date:         {entry['return_date']}")
            print(f"Adults:              {entry['adults']}")
            print(f"Currency:            {entry['currency_code']}")
            print(f"Best Price:          {entry['best_price']}")
            print(f"Stops Allowed:       {entry['stops_allowed']}")
            print(f"Fetched At:          {entry['fetched_at']}\n")

        # Save to database (sync)
        svc.save_temp_prices(entries)
        print("Flight info saved to database.")


if __name__ == '__main__':
    main()
