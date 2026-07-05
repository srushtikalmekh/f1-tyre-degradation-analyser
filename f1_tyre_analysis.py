# ═══════════════════════════════════════════════════════════════════════════════
# F1 Tyre Degradation Analyser — Complete Analysis
# 2023 Bahrain Grand Prix
# Analyses tyre degradation, race strategy, and driver comparisons
# using real F1 timing data via the FastF1 Python library
# ═══════════════════════════════════════════════════════════════════════════════

# ── ALL IMPORTS AT THE TOP ────────────────────────────────────────────────────
import fastf1
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import warnings
import os

warnings.filterwarnings('ignore')

# ── STEP 1: Cache setup ───────────────────────────────────────────────────────
os.makedirs('f1_cache', exist_ok=True)
fastf1.Cache.enable_cache('f1_cache')

# ── STEP 2: Load the race session ONCE ───────────────────────────────────────
# Everything below reuses this same session — no need to reload
print("Loading 2023 Bahrain GP data... (2-3 mins on first run)")
session = fastf1.get_session(2023, 'Bahrain', 'R')
session.load()
print("Race data loaded successfully!\n")

# ── STEP 3: Get all lap data ──────────────────────────────────────────────────
laps = session.laps

# Colour scheme — same as F1 TV broadcasts
compound_colours = {
    'SOFT':         '#FF3333',
    'MEDIUM':       '#FFD700',
    'HARD':         '#FFFFFF',
    'INTERMEDIATE': '#39B54A',
    'WET':          '#0067FF'
}

# ═══════════════════════════════════════════════════════════════════════════════
# FUNCTION: analyse_driver
# Reusable function — call it for any driver instead of repeating code 5 times
# ═══════════════════════════════════════════════════════════════════════════════
def analyse_driver(driver_code):
    print(f"\n{'='*55}")
    print(f"  Analysing: {driver_code}")
    print(f"{'='*55}")

    # Get this driver's clean laps
    driver_laps = laps.pick_driver(driver_code).pick_quicklaps().copy()
    driver_laps['LapTimeSeconds'] = driver_laps['LapTime'].dt.total_seconds()
    driver_laps = driver_laps[driver_laps['LapTimeSeconds'] < 110]

    compounds_used = driver_laps['Compound'].unique()

    print(f"Clean laps: {len(driver_laps)}")
    print(f"Compounds:  {list(compounds_used)}")

    # ── Plot 1: Tyre degradation scatter ─────────────────────────────────────
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor('#1a1a2e')
    ax.set_facecolor('#16213e')

    for compound in compounds_used:
        subset = driver_laps[driver_laps['Compound'] == compound]
        colour = compound_colours.get(compound, '#AAAAAA')
        ax.scatter(subset['TyreLife'], subset['LapTimeSeconds'],
                   label=compound, color=colour, alpha=0.85, s=60,
                   edgecolors='white', linewidths=0.3)

    ax.set_xlabel('Tyre Age (laps)', color='white', fontsize=12)
    ax.set_ylabel('Lap Time (seconds)', color='white', fontsize=12)
    ax.set_title(f'{driver_code} — Tyre Degradation Analysis\n2023 Bahrain Grand Prix',
                 color='white', fontsize=14, fontweight='bold')
    ax.invert_yaxis()
    ax.tick_params(colors='white')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.legend(facecolor='#1a1a2e', labelcolor='white', fontsize=11)
    ax.grid(alpha=0.2, color='white')
    plt.tight_layout()
    plt.savefig(f'scatter_{driver_code}.png', dpi=150,
                bbox_inches='tight', facecolor='#1a1a2e')
    print(f"Saved: scatter_{driver_code}.png")
    plt.show()

    # ── Plot 2: Full race lap times ───────────────────────────────────────────
    fig2, ax2 = plt.subplots(figsize=(14, 6))
    fig2.patch.set_facecolor('#1a1a2e')
    ax2.set_facecolor('#16213e')

    for compound in compounds_used:
        subset = driver_laps[driver_laps['Compound'] == compound]
        colour = compound_colours.get(compound, '#AAAAAA')
        ax2.plot(subset['LapNumber'], subset['LapTimeSeconds'],
                 color=colour, linewidth=2, marker='o',
                 markersize=4, label=compound)

    ax2.set_xlabel('Lap Number', color='white', fontsize=12)
    ax2.set_ylabel('Lap Time (seconds)', color='white', fontsize=12)
    ax2.set_title(f'{driver_code} — Lap Times Across Full Race\n2023 Bahrain Grand Prix',
                  color='white', fontsize=14, fontweight='bold')
    ax2.invert_yaxis()
    ax2.tick_params(colors='white')
    ax2.spines['bottom'].set_color('white')
    ax2.spines['left'].set_color('white')
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.legend(facecolor='#1a1a2e', labelcolor='white', fontsize=11)
    ax2.grid(alpha=0.2, color='white')
    plt.tight_layout()
    plt.savefig(f'race_{driver_code}.png', dpi=150,
                bbox_inches='tight', facecolor='#1a1a2e')
    print(f"Saved: race_{driver_code}.png")
    plt.show()

    # ── Degradation rate calculation ──────────────────────────────────────────
    print(f"\n── Degradation Rate — {driver_code} ──")
    print(f"{'Compound':<15} {'Avg Time':>10} {'Laps':>6} {'Deg Rate':>15}")
    print("-" * 50)

    for compound in compounds_used:
        subset = driver_laps[driver_laps['Compound'] == compound].copy()
        if len(subset) > 2:
            z = np.polyfit(subset['TyreLife'], subset['LapTimeSeconds'], 1)
            avg_time = subset['LapTimeSeconds'].mean()
            print(f"{compound:<15} {avg_time:>10.3f}s {len(subset):>6}"
                  f" {z[0]:>+15.3f} s/lap")


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 1: Individual driver analysis
# Add or remove drivers from this list freely
# ═══════════════════════════════════════════════════════════════════════════════
drivers_to_analyse = ['VER', 'LEC', 'HAM', 'SAI', 'ALO']

for driver in drivers_to_analyse:
    analyse_driver(driver)


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 2: Race results — Top 10
# ═══════════════════════════════════════════════════════════════════════════════
print("\n\n── 2023 Bahrain GP — Top 10 Race Results ──")
results = session.results[['Position', 'FullName', 'TeamName', 'Status']].copy()
results = results.sort_values('Position')

print(f"\n{'Pos':<5} {'Driver':<25} {'Team':<30} {'Status'}")
print("-" * 75)
for _, row in results.head(10).iterrows():
    print(f"{int(row['Position']):<5} {row['FullName']:<25}"
          f" {row['TeamName']:<30} {row['Status']}")


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 3: All drivers — Hard tyre degradation bar chart
# ═══════════════════════════════════════════════════════════════════════════════
print("\n\n── Hard Tyre Degradation — All Drivers ──")

def compound_bar_chart(compound_name, filename, highlight_driver='VER'):
    all_drivers = laps['Driver'].unique()
    deg_data = []

    for driver in all_drivers:
        d = laps.pick_driver(driver).pick_quicklaps().copy()
        d = d[d['Compound'] == compound_name]
        d['LapTimeSeconds'] = d['LapTime'].dt.total_seconds()

        if len(d) > 3:
            z = np.polyfit(d['TyreLife'], d['LapTimeSeconds'], 1)
            deg_data.append({'Driver': driver, 'DegRate': z[0]})

    if not deg_data:
        print(f"Not enough data for {compound_name} chart")
        return

    deg_df = pd.DataFrame(deg_data).sort_values('DegRate')

    fig, ax = plt.subplots(figsize=(14, 6))
    fig.patch.set_facecolor('#1a1a2e')
    ax.set_facecolor('#16213e')

    colours = ['#FF3333' if d == highlight_driver else '#4FC3F7'
               for d in deg_df['Driver']]
    ax.bar(deg_df['Driver'], deg_df['DegRate'], color=colours)

    ax.set_xlabel('Driver', color='white', fontsize=12)
    ax.set_ylabel('Degradation Rate (s/lap)', color='white', fontsize=12)
    ax.set_title(f'{compound_name} Tyre Degradation Rate — All Drivers\n2023 Bahrain GP',
                 color='white', fontsize=14, fontweight='bold')
    ax.tick_params(colors='white')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(alpha=0.2, color='white', axis='y')
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight', facecolor='#1a1a2e')
    print(f"Saved: {filename}")
    plt.show()

# Generate both compound charts
compound_bar_chart('HARD', 'all_drivers_hard_degradation.png')
compound_bar_chart('SOFT', 'all_drivers_soft_degradation.png')


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 4: Pit stop analysis — full field
# ═══════════════════════════════════════════════════════════════════════════════
print("\n\n── Pit Stop Summary — 2023 Bahrain GP ──")
print(f"{'Driver':<8} {'Pit Lap':<10} {'Tyre Off':<14} {'Tyre On'}")
print("-" * 45)

all_driver_codes = ['VER', 'LEC', 'HAM', 'SAI', 'PER', 'ALO',
                    'TSU', 'NOR', 'GAS', 'RUS', 'BOT', 'HUL',
                    'STR', 'ALB', 'ZHO', 'SAR', 'DEV', 'MAG', 'OCO']

for driver in all_driver_codes:
    d_laps = laps.pick_driver(driver).copy()
    d_laps = d_laps.sort_values('LapNumber').reset_index(drop=True)
    for i in range(1, len(d_laps)):
        curr = d_laps.loc[i, 'Compound']
        prev = d_laps.loc[i - 1, 'Compound']
        if curr != prev:
            print(f"{driver:<8} {int(d_laps.loc[i,'LapNumber']):<10}"
                  f" {prev:<14} {curr}")

print("\n── Pit Stop Count Per Driver ──")
print(f"{'Driver':<8} {'Stops'}")
print("-" * 16)
for driver in all_driver_codes:
    d_laps = laps.pick_driver(driver).copy()
    d_laps = d_laps.sort_values('LapNumber').reset_index(drop=True)
    count = sum(1 for i in range(1, len(d_laps))
                if d_laps.loc[i, 'Compound'] != d_laps.loc[i-1, 'Compound'])
    print(f"{driver:<8} {count}")


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 5: Team comparison — Red Bull vs Ferrari (Hard tyre)
# ═══════════════════════════════════════════════════════════════════════════════
print("\n\n── Team Comparison: Red Bull vs Ferrari — Hard Tyre ──")

team_drivers = {
    'Red Bull': {'drivers': ['VER', 'PER'],
                 'colours': ['#3671C6', '#6BAEED']},
    'Ferrari':  {'drivers': ['LEC', 'SAI'],
                 'colours': ['#E8002D', '#FF6B6B']}
}

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.patch.set_facecolor('#1a1a2e')
fig.suptitle('Red Bull vs Ferrari — Hard Tyre Pace\n2023 Bahrain Grand Prix',
             color='white', fontsize=14, fontweight='bold', y=1.02)

for idx, (team, info) in enumerate(team_drivers.items()):
    ax = axes[idx]
    ax.set_facecolor('#16213e')

    for driver, colour in zip(info['drivers'], info['colours']):
        d_hard = laps.pick_driver(driver).pick_quicklaps().copy()
        d_hard = d_hard[d_hard['Compound'] == 'HARD']
        d_hard['LapTimeSeconds'] = d_hard['LapTime'].dt.total_seconds()

        if len(d_hard) > 0:
            ax.scatter(d_hard['TyreLife'], d_hard['LapTimeSeconds'],
                       label=driver, color=colour, alpha=0.85, s=60,
                       edgecolors='white', linewidths=0.3)

            if len(d_hard) > 2:
                z = np.polyfit(d_hard['TyreLife'], d_hard['LapTimeSeconds'], 1)
                p = np.poly1d(z)
                x_line = np.linspace(d_hard['TyreLife'].min(),
                                     d_hard['TyreLife'].max(), 100)
                ax.plot(x_line, p(x_line), color=colour,
                        linewidth=2, linestyle='--', alpha=0.7)
                print(f"{team} | {driver} Hard deg rate: {z[0]:+.3f} s/lap")

    ax.set_title(team, color='white', fontsize=13, fontweight='bold')
    ax.set_xlabel('Tyre Age (laps)', color='white', fontsize=11)
    ax.set_ylabel('Lap Time (seconds)', color='white', fontsize=11)
    ax.tick_params(colors='white')
    ax.invert_yaxis()
    ax.legend(facecolor='#1a1a2e', labelcolor='white', fontsize=11)
    ax.grid(alpha=0.2, color='white')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')

plt.tight_layout()
plt.savefig('team_comparison_hard_tyre.png', dpi=150,
            bbox_inches='tight', facecolor='#1a1a2e')
print("Saved: team_comparison_hard_tyre.png")
plt.show()


# ═══════════════════════════════════════════════════════════════════════════════
# DONE — Summary of all saved files
# ═══════════════════════════════════════════════════════════════════════════════
print("\n\n── Analysis Complete ──")
print("Files saved:")
print("  scatter_VER.png          — VER tyre degradation scatter")
print("  race_VER.png             — VER full race lap times")
print("  scatter_LEC.png          — LEC tyre degradation scatter")
print("  race_LEC.png             — LEC full race lap times")
print("  scatter_HAM.png          — HAM tyre degradation scatter")
print("  race_HAM.png             — HAM full race lap times")
print("  scatter_SAI.png          — SAI tyre degradation scatter")
print("  race_SAI.png             — SAI full race lap times")
print("  scatter_ALO.png          — ALO tyre degradation scatter")
print("  race_ALO.png             — ALO full race lap times")
print("  all_drivers_hard_degradation.png  — full field Hard tyre chart")
print("  all_drivers_soft_degradation.png  — full field Soft tyre chart")
print("  team_comparison_hard_tyre.png     — Red Bull vs Ferrari")
print("\nUpload all files + README.md to GitHub.")