import streamlit as st
import pandas as pd
import time

# Set page configuration
st.set_page_config(
    page_title="Molecular Docking Application",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #2e8b57;
        border-bottom: 2px solid #2e8b57;
        padding-bottom: 0.5rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #f0f8ff;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #f0fff0;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #32cd32;
        margin: 1rem 0;
    }
    .search-box {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #e9ecef;
        margin: 1rem 0;
    }
    .upload-box {
        background-color: #f0f8ff;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #b6d7ff;
        margin: 1rem 0;
    }
    .docking-box {
        background-color: #fff5f5;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #fed7d7;
        margin: 1rem 0;
    }
    .nav-button {
        margin: 0.2rem;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        border: none;
        background-color: #1f77b4;
        color: white;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = "main"
if 'docking_results' not in st.session_state:
    st.session_state.docking_results = None
if 'protein_selected' not in st.session_state:
    st.session_state.protein_selected = None
if 'ligand_selected' not in st.session_state:
    st.session_state.ligand_selected = None

def simulate_docking_results():
    """Generate simulated docking results"""
    results = []
    for i in range(10):  # Generate 10 poses
        results.append({
            'Pose': i + 1,
            'Binding_Affinity_kcal_mol': round(-8.5 + i * 0.3 + (i * 0.1), 2),
            'RMSD_l.b.': round(0.0 + i * 0.2, 2),
            'RMSD_u.b.': round(0.5 + i * 0.3, 2),
            'Efficiency': round(0.95 - i * 0.05, 3)
        })
    return pd.DataFrame(results)

def main():
    st.markdown('<h1 class="main-header">🧬 Molecular Docking Application</h1>', unsafe_allow_html=True)
    
    # Navigation buttons at the top
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 2])
    
    with col1:
        if st.button("🏠 Main Dashboard", type="primary" if st.session_state.current_page == "main" else "secondary"):
            st.session_state.current_page = "main"
    
    with col2:
        if st.button("📊 Results", type="primary" if st.session_state.current_page == "results" else "secondary"):
            st.session_state.current_page = "results"
    
    with col3:
        if st.button("ℹ️ Help", type="primary" if st.session_state.current_page == "help" else "secondary"):
            st.session_state.current_page = "help"
    
    # Display current page content
    if st.session_state.current_page == "main":
        main_dashboard()
    elif st.session_state.current_page == "results":
        results_page()
    elif st.session_state.current_page == "help":
        help_page()

def main_dashboard():
    # Welcome section
    st.markdown("""
    <div class="info-box">
    <h3>🎯 Welcome to Molecular Docking Platform</h3>
    <p>Search for proteins and ligands, upload custom files, and run molecular docking simulations all from one place!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Search and Upload sections in columns
    col1, col2 = st.columns(2)
    
    # Protein Section (Search + Upload)
    with col1:
        st.markdown("""
        <div class="search-box">
        <h3>🔍 Protein Search & Upload</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Tab-like interface for search vs upload
        protein_option = st.radio("Choose option:", ["🔍 Search Database", "📁 Upload File"], 
                                 key="protein_option", horizontal=True)
        
        if protein_option == "🔍 Search Database":
            protein_query = st.text_input("Enter protein name or PDB ID:", 
                                        placeholder="e.g., insulin, 1A2B, hemoglobin", 
                                        key="protein_search")
            
            if st.button("Search Proteins", type="primary", key="search_proteins"):
                if protein_query:
                    with st.spinner("Searching PDB database..."):
                        time.sleep(2)  # Simulate search
                    
                    # Mock protein results
                    proteins = [
                        {"id": "1A2B", "name": "Insulin Receptor", "resolution": "2.1 Å"},
                        {"id": "3C4D", "name": "Hemoglobin Alpha Chain", "resolution": "1.8 Å"},
                        {"id": "5E6F", "name": "Protein Kinase", "resolution": "2.5 Å"}
                    ]
                    
                    st.success(f"Found {len(proteins)} proteins matching '{protein_query}'")
                    
                    selected_protein = st.selectbox(
                        "Select a protein:",
                        options=[f"{p['id']} - {p['name']} ({p['resolution']})" for p in proteins],
                        key="protein_selector"
                    )
                    
                    if st.button("Select This Protein", key="select_protein"):
                        st.session_state.protein_selected = selected_protein
                        st.success(f"✅ Selected: {selected_protein}")
        
        else:  # Upload File
            st.markdown("""
            <div class="upload-box">
            <h4>📁 Upload Protein File</h4>
            </div>
            """, unsafe_allow_html=True)
            
            protein_file = st.file_uploader(
                "Choose protein file", 
                type=['pdb', 'pdbqt'],
                help="Upload PDB or PDBQT format protein files",
                key="protein_upload"
            )
            
            if protein_file is not None:
                st.session_state.protein_selected = f"Uploaded: {protein_file.name}"
                st.success(f"✅ {protein_file.name} uploaded successfully!")
    
    # Ligand Section (Search + Upload)
    with col2:
        st.markdown("""
        <div class="search-box">
        <h3>💊 Ligand Search & Upload</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Tab-like interface for search vs upload
        ligand_option = st.radio("Choose option:", ["🔍 Search Database", "📁 Upload File"], 
                                key="ligand_option", horizontal=True)
        
        if ligand_option == "🔍 Search Database":
            ligand_query = st.text_input("Enter ligand name:", 
                                       placeholder="e.g., aspirin, caffeine, glucose", 
                                       key="ligand_search")
            
            if st.button("Search Ligands", type="primary", key="search_ligands"):
                if ligand_query:
                    with st.spinner("Searching PubChem database..."):
                        time.sleep(2)  # Simulate search
                    
                    # Mock ligand results
                    ligands = [
                        {"cid": "2244", "name": "Aspirin", "formula": "C9H8O4", "weight": "180.16"},
                        {"cid": "2519", "name": "Caffeine", "formula": "C8H10N4O2", "weight": "194.19"},
                        {"cid": "5793", "name": "Glucose", "formula": "C6H12O6", "weight": "180.16"}
                    ]
                    
                    st.success(f"Found {len(ligands)} ligands matching '{ligand_query}'")
                    
                    selected_ligand = st.selectbox(
                        "Select a ligand:",
                        options=[f"CID {l['cid']} - {l['name']} ({l['formula']})" for l in ligands],
                        key="ligand_selector"
                    )
                    
                    if st.button("Select This Ligand", key="select_ligand"):
                        st.session_state.ligand_selected = selected_ligand
                        st.success(f"✅ Selected: {selected_ligand}")
        
        else:  # Upload File
            st.markdown("""
            <div class="upload-box">
            <h4>📁 Upload Ligand File</h4>
            </div>
            """, unsafe_allow_html=True)
            
            ligand_file = st.file_uploader(
                "Choose ligand file", 
                type=['sdf', 'mol', 'mol2', 'pdbqt'],
                help="Upload SDF, MOL, MOL2, or PDBQT format ligand files",
                key="ligand_upload"
            )
            
            if ligand_file is not None:
                st.session_state.ligand_selected = f"Uploaded: {ligand_file.name}"
                st.success(f"✅ {ligand_file.name} uploaded successfully!")
    
    # Current Selection Status
    st.markdown('<div class="section-header">📋 Current Selection</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.session_state.protein_selected:
            st.info(f"🧬 **Protein:** {st.session_state.protein_selected}")
        else:
            st.warning("⚠️ No protein selected")
    
    with col2:
        if st.session_state.ligand_selected:
            st.info(f"💊 **Ligand:** {st.session_state.ligand_selected}")
        else:
            st.warning("⚠️ No ligand selected")
    
    # Docking Section
    st.markdown("""
    <div class="docking-box">
    <h3>⚡ Molecular Docking Configuration & Execution</h3>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.protein_selected and st.session_state.ligand_selected:
        # Docking parameters in a more compact layout
        st.subheader("🔧 Docking Parameters")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            exhaustiveness = st.slider("Exhaustiveness", 1, 32, 8, 
                                     help="Thoroughness of the search")
            num_modes = st.slider("Number of Modes", 1, 20, 9, 
                                help="Number of binding modes to generate")
        
        with col2:
            energy_range = st.slider("Energy Range (kcal/mol)", 1, 10, 3, 
                                   help="Maximum energy difference between modes")
            box_size = st.slider("Search Box Size (Å)", 10, 40, 20,
                                help="Size of the search space")
        
        with col3:
            center_x = st.number_input("Center X", value=0.0, format="%.2f")
            center_y = st.number_input("Center Y", value=0.0, format="%.2f")
            center_z = st.number_input("Center Z", value=0.0, format="%.2f")
        
        # Run docking button - prominent and centered
        st.markdown("### 🚀 Execute Docking")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Run Molecular Docking", type="primary", key="run_docking", 
                        help="Start the molecular docking simulation"):
                st.info("🔄 Starting molecular docking simulation...")
                
                # Simulate docking process
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                stages = [
                    "Preparing protein structure...",
                    "Preparing ligand structure...",
                    "Setting up docking parameters...",
                    "Running docking simulation...",
                    "Analyzing binding poses...",
                    "Generating final results..."
                ]
                
                for i, stage in enumerate(stages):
                    status_text.text(f"⏳ {stage}")
                    progress_bar.progress((i + 1) / len(stages))
                    time.sleep(1.2)
                
                # Generate and store results
                st.session_state.docking_results = simulate_docking_results()
                
                status_text.text("✅ Docking simulation completed successfully!")
                st.success("🎉 Molecular docking simulation completed!")
                st.balloons()
                
                # Show quick results preview
                df = st.session_state.docking_results
                best_pose = df.loc[df['Binding_Affinity_kcal_mol'].idxmin()]
                
                st.markdown("### 📈 Quick Results Preview")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Poses", len(df), "Generated")
                with col2:
                    st.metric("Best Binding Affinity", f"{best_pose['Binding_Affinity_kcal_mol']} kcal/mol", "Strongest")
                with col3:
                    st.metric("Best Pose RMSD", f"{best_pose['RMSD_l.b.']} Å", "Deviation")
                with col4:
                    st.metric("Top Efficiency", f"{best_pose['Efficiency']:.3f}", "Score")
                
                # Quick actions
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📊 View Detailed Results", type="secondary"):
                        st.session_state.current_page = "results"
                        st.rerun()
                with col2:
                    csv_data = df.to_csv(index=False)
                    st.download_button(
                        label="💾 Download Results (CSV)",
                        data=csv_data,
                        file_name="docking_results.csv",
                        mime="text/csv",
                        type="secondary"
                    )
    else:
        st.markdown("""
        <div style='text-align: center; padding: 2rem; background-color: #fff3cd; border-radius: 0.5rem; margin: 1rem 0;'>
        <h4>⚠️ Ready to Start Docking?</h4>
        <p>Please select or upload both a protein and a ligand above to configure and run the molecular docking simulation.</p>
        </div>
        """, unsafe_allow_html=True)

def results_page():
    st.markdown('<div class="section-header">📊 Docking Results & Analysis</div>', unsafe_allow_html=True)
    
    if st.session_state.docking_results is not None:
        df = st.session_state.docking_results
        
        # Display summary metrics
        st.subheader("📈 Summary Dashboard")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Poses", len(df), "Generated")
        with col2:
            best_affinity = df['Binding_Affinity_kcal_mol'].min()
            st.metric("Best Binding Affinity", f"{best_affinity} kcal/mol", "Strongest")
        with col3:
            avg_rmsd = df['RMSD_l.b.'].mean()
            st.metric("Average RMSD (l.b.)", f"{avg_rmsd:.2f} Å", "Deviation")
        with col4:
            best_efficiency = df['Efficiency'].max()
            st.metric("Highest Efficiency", f"{best_efficiency:.3f}", "Score")
        
        # Input information
        st.subheader("🔍 Docking Input Summary")
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"🧬 **Protein:** {st.session_state.protein_selected or 'Not specified'}")
        with col2:
            st.info(f"💊 **Ligand:** {st.session_state.ligand_selected or 'Not specified'}")
        
        # Results table
        st.subheader("📋 Detailed Results Table")
        st.dataframe(
            df.style.highlight_min(subset=['Binding_Affinity_kcal_mol'], color='lightgreen')
            .highlight_max(subset=['Efficiency'], color='lightblue'),
            use_container_width=True
        )
        
        # Visualizations
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📊 Binding Affinity by Pose")
            st.line_chart(df.set_index('Pose')['Binding_Affinity_kcal_mol'])
        
        with col2:
            st.subheader("📊 RMSD vs Binding Affinity")
            st.scatter_chart(df.set_index('RMSD_l.b.')['Binding_Affinity_kcal_mol'])
        
        # Download section
        st.subheader("💾 Export & Download")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            csv_data = df.to_csv(index=False)
            st.download_button(
                label="📥 Download Results (CSV)",
                data=csv_data,
                file_name="docking_results.csv",
                mime="text/csv",
                type="primary"
            )
        
        with col2:
            # Create a summary report
            report = f"""# Molecular Docking Results Report

## Input Information
- Protein: {st.session_state.protein_selected or 'Not specified'}
- Ligand: {st.session_state.ligand_selected or 'Not specified'}
- Timestamp: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary Statistics
- Total Poses Generated: {len(df)}
- Best Binding Affinity: {best_affinity} kcal/mol
- Average RMSD (l.b.): {avg_rmsd:.2f} Å
- Highest Efficiency: {best_efficiency:.3f}

## Top 5 Binding Poses
{df.head(5).to_string(index=False)}

## Analysis Notes
- Lower binding affinity values indicate stronger protein-ligand binding
- RMSD values show structural deviation from reference pose
- Efficiency metric combines binding strength and structural quality
- Results are ordered by binding affinity (strongest first)

## Recommendations
- Focus on poses 1-3 for further analysis
- Consider experimental validation of top-ranked poses
- Review binding site interactions for optimization opportunities
"""
            st.download_button(
                label="📄 Download Report (TXT)",
                data=report,
                file_name="docking_analysis_report.txt",
                mime="text/plain"
            )
        
        with col3:
            if st.button("🔄 Run New Docking", type="secondary"):
                st.session_state.current_page = "main"
                st.rerun()
    
    else:
        st.markdown("""
        <div style='text-align: center; padding: 3rem; background-color: #f8f9fa; border-radius: 0.5rem;'>
        <h3>🔍 No Results Available</h3>
        <p>No docking results to display. Please run a molecular docking simulation first.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📋 How to Generate Results:")
        st.markdown("""
        1. **Go to Main Dashboard** - Use the navigation button above
        2. **Select/Upload Protein** - Search database or upload your own file
        3. **Select/Upload Ligand** - Search database or upload your own file  
        4. **Configure Parameters** - Set docking parameters as needed
        5. **Run Simulation** - Click the "Run Molecular Docking" button
        6. **View Results** - Return here to analyze your results
        """)
        
        if st.button("🏠 Go to Main Dashboard", type="primary"):
            st.session_state.current_page = "main"
            st.rerun()

def help_page():
    st.markdown('<div class="section-header">ℹ️ Help & Documentation</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ## 🧬 About Molecular Docking
    
    Molecular docking is a computational method that predicts the preferred orientation of one molecule (ligand) 
    when bound to another (protein) to form a stable complex. This application simulates the docking process 
    and provides binding affinity scores and structural analysis.
    
    ## 🔧 How to Use This Application
    
    ### Step 1: Select Your Molecules
    - **Protein**: Search PDB database or upload your own PDB/PDBQT file
    - **Ligand**: Search PubChem database or upload SDF/MOL/MOL2/PDBQT file
    
    ### Step 2: Configure Docking Parameters
    - **Exhaustiveness**: Controls search thoroughness (higher = more accurate, slower)
    - **Number of Modes**: How many binding poses to generate
    - **Energy Range**: Maximum energy difference between poses
    - **Binding Site**: Center coordinates and search box size
    
    ### Step 3: Run Simulation
    - Click "Run Molecular Docking" to start the process
    - Monitor progress through the status updates
    - Review quick results preview
    
    ### Step 4: Analyze Results
    - View detailed results in the Results section
    - Download data as CSV or formatted report
    - Interpret binding affinities and RMSD values
    
    ## 📊 Understanding Results
    
    ### Key Metrics:
    - **Binding Affinity (kcal/mol)**: Lower values indicate stronger binding
    - **RMSD (Å)**: Root Mean Square Deviation - structural variation from reference
    - **Efficiency**: Combined score of binding strength and structural quality
    
    ### Interpretation:
    - **Strong Binding**: Affinity < -7.0 kcal/mol
    - **Moderate Binding**: Affinity -7.0 to -5.0 kcal/mol  
    - **Weak Binding**: Affinity > -5.0 kcal/mol
    
    ## 📁 Supported File Formats
    
    ### Proteins:
    - **PDB**: Protein Data Bank format (most common)
    - **PDBQT**: AutoDock format with charges and atom types
    
    ### Ligands:
    - **SDF**: Structure Data Format
    - **MOL**: MDL Molfile format
    - **MOL2**: Tripos molecular format
    - **PDBQT**: AutoDock format for ligands
    
    ## 🎯 Tips for Best Results
    
    1. **Use high-resolution protein structures** (< 2.5 Å resolution)
    2. **Ensure binding site coordinates are accurate** 
    3. **Start with default parameters** and adjust based on needs
    4. **Consider multiple conformations** by increasing number of modes
    5. **Validate results** with experimental data when possible
    
    ## ⚠️ Limitations
    
    - This is a **simulation interface** - actual docking requires backend setup
    - Results shown are **demonstration data** for interface testing
    - For production use, integrate with AutoDock Vina or similar tools
    - Consider protein flexibility and solvent effects in real applications
    
    ## 🔗 External Resources
    
    - **PDB Database**: https://www.rcsb.org/
    - **PubChem**: https://pubchem.ncbi.nlm.nih.gov/
    - **AutoDock Vina**: https://vina.scripps.edu/
    - **PyMOL**: https://pymol.org/ (for visualization)
    
    ## 📧 Support
    
    For technical support or questions about molecular docking:
    - Check documentation of your docking software
    - Consult computational chemistry resources
    - Consider professional bioinformatics support for complex projects
    """)
    
    # Quick reference cards
    st.markdown("## 🚀 Quick Reference")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🔍 Search Tips
        - Use protein names or PDB IDs
        - Try common drug names for ligands
        - Check spelling and use alternatives
        - Browse results before selecting
        """)
    
    with col2:
        st.markdown("""
        ### ⚡ Docking Tips
        - Higher exhaustiveness = better results
        - Use 9-20 modes for thorough search
        - Center binding site accurately
        - Allow adequate search space
        """)
    
    with col3:
        st.markdown("""
        ### 📊 Analysis Tips
        - Focus on top 3-5 poses
        - Compare binding affinities
        - Check RMSD for consistency
        - Download data for further analysis
        """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray; font-size: 0.8rem; margin-top: 2rem;'>"
    "🧬 Molecular Docking Application | Streamlit Frontend Interface | "
    "For demonstration and educational purposes"
    "</div>", 
    unsafe_allow_html=True
)

if __name__ == "__main__":
    main()