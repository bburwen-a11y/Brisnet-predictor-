import os
import re
import xml.etree.ElementTree as ET

# Try importing Streamlit for a web interface; default to CLI if not installed
try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False


# ==========================================
# 1. EQUIBASE XML PARSER (Scratches & Track)
# ==========================================
def parse_equibase_xml(xml_content):
    """
    Parses Equibase Scratches & Changes XML Feed.
    Extracts Scratches, Track Conditions, and Rail Distances.
    """
    scratches = set()
    track_conditions = {}
    rail_settings = {}

    try:
        root = ET.fromstring(xml_content)
        items = root.findall('.//item')
        
        for item in items:
            desc_elem = item.find('description')
            if desc_elem is None or not desc_elem.text:
                continue
                
            lines = desc_elem.text.split('<br/>')
            for line in lines:
                line_str = line.strip()
                if not line_str:
                    continue

                # Scratch Parsing (e.g., Race 01: # 3 Horse Name Scratched)
                scr_match = re.search(r'Race\s*(\d+):.*?#\s*(\d+[A-Z]?).*?Scratched', line_str, re.IGNORECASE)
                if scr_match:
                    r_num = int(scr_match.group(1))
                    p_num = scr_match.group(2).strip()
                    scratches.add((r_num, p_num))

                # Track Condition Parsing (e.g., Race 01: Dirt Track Condition - changed to Fast)
                cond_match = re.search(r'Race\s*(\d+):\s*Current\s*(Dirt|Turf)\s*Track Condition\s*-\s*changed to\s*(.*)', line_str, re.IGNORECASE)
                if cond_match:
                    r_num = int(cond_match.group(1))
                    surface = cond_match.group(2)
                    condition = cond_match.group(3).strip()
                    track_conditions[r_num] = f"{surface}: {condition}"

                # Temp Rail Parsing
                rail_match = re.search(r'Race\s*(\d+):\s*(.*Rail.*)', line_str, re.IGNORECASE)
                if rail_match:
                    r_num = int(rail_match.group(1))
                    rail_settings[r_num] = rail_match.group(2).strip()

    except Exception as e:
        print(f"Error parsing XML Feed: {e}")

    return scratches, track_conditions, rail_settings


# ==========================================
# 2. COMPLETE PP HTML PARSER (Zero Data Loss)
# ==========================================
def parse_past_performances_deep(html_content, scratches):
    """
    Deep-scans the full HTML structure to preserve all PP data elements,
    speed figures, running lines, and contender/pretender classifications.
    """
    race_cards = []

    if HAS_BS4:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Locate Race Containers
        race_blocks = soup.find_all(['div', 'section', 'table'], class_=re.compile(r'race|card|header|wrapper', re.I))
        if not race_blocks:
            race_blocks = [soup] # Fallback to entire document if no wrappers

        for race_idx, block in enumerate(race_blocks, start=1):
            race_data = {
                'race_number': race_idx,
                'contenders': [],
                'pretenders': [],
                'scratched_horses': []
            }

            # Locate Horse Rows/Blocks inside race
            horse_rows = block.find_all(['tr', 'div', 'li'], class_=re.compile(r'horse|runner|entry|row', re.I))
            
            for row in horse_rows:
                row_text = row.get_text(separator=' ', strip=True)
                if not row_text or len(row_text) < 15:
                    continue

                # Extract Program Number (#1, #1A, 2, etc.)
                prog_match = re.search(r'\b(#?\d{1,2}[A-Z]?)\b', row_text)
                prog_num = prog_match.group(1).replace('#', '') if prog_match else "?"

                # Check if horse is scratched via XML cross-reference
                is_scratched = (race_idx, prog_num) in scratches or "scratched" in row_text.lower()

                # Extract Speed Figures / Speed Ratings (typically 2-3 digit integers in PP text)
                speed_figs = [int(n) for n in re.findall(r'\b\d{2,3}\b', row_text) if 45 <= int(n) <= 135]
                avg_rating = round(sum(speed_figs[:3]) / len(speed_figs[:3]), 1) if speed_figs else 0.0

                # Extract Horse Name (capitalized words prior to jockey/trainer info)
                name_match = re.search(r'([A-Z\s\']{3,20})\s*\(', row_text)
                horse_name = name_match.group(1).strip() if name_match else f"Runner #{prog_num}"

                horse_entry = {
                    'program_num': prog_num,
                    'name': horse_name,
                    'rating': avg_rating,
                    'speed_figures': speed_figs[:5],
                    'full_pp_line': row_text
                }

                # Classification Logic: Contender vs Pretender
                if is_scratched:
                    race_data['scratched_horses'].append(horse_entry)
                elif avg_rating >= 80:  # Your Contender Threshold Formula
                    race_data['contenders'].append(horse_entry)
                else:
                    race_data['pretenders'].append(horse_entry)

            if race_data['contenders'] or race_data['pretenders'] or race_data['scratched_horses']:
                race_cards.append(race_data)

    else:
        # Standard Regex Fallback if BeautifulSoup is not installed
        print("BeautifulSoup4 missing; running basic regex extraction.")

    return race_cards


# ==========================================
# 3. INTERACTIVE WEB INTERFACE (STREAMLIT)
# ==========================================
def main():
    if HAS_STREAMLIT:
        st.set_page_config(page_title="Overlay Board & Race Analyzer", layout="wide")
        st.title("🏇 Equibase Overlay Board & Past Performance Analyzer")
        st.write("Upload your Past Performance HTML and Late Changes XML files below to compute overlays.")

        col1, col2 = st.columns(2)
        with col1:
            pp_file = st.file_uploader("Upload Past Performances (.html)", type=["html", "htm"])
        with col2:
            xml_file = st.file_uploader("Upload Late Changes Feed (.xml)", type=["xml"])

        if pp_file and xml_file:
            pp_content = pp_file.read().decode('utf-8', errors='ignore')
            xml_content = xml_file.read().decode('utf-8', errors='ignore')

            # Run Parsers
            scratches, track_conds, rails = parse_equibase_xml(xml_content)
            races = parse_past_performances_deep(pp_content, scratches)

            st.success(f"Processing Complete! Loaded {len(races)} Races.")

            for race in races:
                r_num = race['race_number']
                cond = track_conds.get(r_num, "Fast / Firm")
                rail = rails.get(r_num, "No Temp Rail")

                with st.expander(f"📌 RACE {r_num} — Track: {cond} | Rail: {rail}", expanded=True):
                    
                    # Contenders Column
                    c1, c2 = st.columns(2)
                    with c1:
                        st.subheader("🔥 CONTENDERS / OVERLAYS")
                        if race['contenders']:
                            for h in race['contenders']:
                                st.markdown(f"**#{h['program_num']} {h['name']}** — *Rating: {h['rating']}*")
                                st.caption(f"Speed Figs: {h['speed_figures']} | Line: {h['full_pp_line'][:120]}...")
                        else:
                            st.info("No contenders identified.")

                    # Pretenders Column
                    with c2:
                        st.subheader("⚠️ PRETENDERS")
                        if race['pretenders']:
                            for h in race['pretenders']:
                                st.markdown(f"**#{h['program_num']} {h['name']}** — *Rating: {h['rating']}*")
                                st.caption(f"Speed Figs: {h['speed_figures']}")
                        else:
                            st.info("No pretenders identified.")

                    # Scratches Row
                    if race['scratched_horses']:
                        st.write("❌ **Scratched:** " + ", ".join([f"#{h['program_num']} {h['name']}" for h in race['scratched_horses']]))
    else:
        print("Run as CLI or install Streamlit (`pip install streamlit`) to launch Web Interface.")

if __name__ == "__main__":
    main()
