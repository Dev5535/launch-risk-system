import streamlit as st
import sys
import os
import json
import pandas as pd

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
# Add web_ui to path for layout
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from product_1_digital_twin_auditor.src.crawler import Crawler
from product_1_digital_twin_auditor.src.analyzer import Analyzer
from layout import render_support_sidebar, render_footer

st.set_page_config(page_title="Digital Twin Auditor", page_icon="🔍")

render_support_sidebar()

st.header("🔍 Product 1: Digital Twin Pre-Migration Auditor")
st.markdown("**User:** IT Manager / DevOps | **Goal:** Detect Config Drift & Asset Mismatches")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Source Environment (Staging)")
    source_path = st.text_input("Source Path (Local or URL)", value="./staging")

with col2:
    st.subheader("Target Environment (Production)")
    target_path = st.text_input("Target Path (Local or URL)", value="./prod")

if st.button("🚀 Run Configuration Audit"):
    with st.spinner("Crawling environments..."):
        # 1. Crawl
        crawler = Crawler(source_path) # Pass source_path to constructor
        try:
            source_data = crawler.crawl() # Use .crawl() not .scan()
            
            crawler_target = Crawler(target_path)
            target_data = crawler_target.crawl()
            
            # 2. Analyze
            # Analyzer expects dicts with 'files' key, but crawler returns dict of Assets
            # Need to adapt or update Analyzer. Let's update Analyzer call or wrap data
            # P1 Analyzer usually expects list of file paths or similar.
            # Let's check P1/src/analyzer.py briefly.
            # Assuming Analyzer expects {path: content_hash} or similar.
            # Let's mock the adapter here for speed
            
            # src_dict = {'files': {k: v.content_hash for k, v in source_data.items()}}
            # tgt_dict = {'files': {k: v.content_hash for k, v in target_data.items()}}
            
            # delta = analyzer.compare(src_dict, tgt_dict)
            
            # CORRECT FIX: Analyzer takes (source_assets, target_assets) in constructor and has analyze() method
            analyzer = Analyzer(source_data, target_data)
            delta = analyzer.analyze()
            
            st.success("Audit Complete!")
            
            # Store in session for P4/P5
            report = {'delta': delta, 'timestamp': str(pd.Timestamp.now())}
            st.session_state['p1_report'] = report
            
            # Display Results
            st.subheader("📊 Audit Findings")
            
            # Metrics
            m1, m2, m3 = st.columns(3)
            m1.metric("Files Scanned", len(source_data.get('files', [])) + len(target_data.get('files', [])))
            m2.metric("Missing in Prod", len(delta.get('removed_in_prod', [])))
            m3.metric("Modified Content", len(delta.get('modified', [])))
            
            # Tabs for details
            tab1, tab2, tab3, tab4 = st.tabs(["❌ Missing Assets", "⚠️ Config Drift", "🕸️ Dependency Map", "🕵️ Shadow IT"])
            
            with tab1:
                if delta.get('removed_in_prod'):
                    st.error("The following files exist in Staging but are MISSING in Production:")
                    st.table(pd.DataFrame(delta['removed_in_prod'], columns=["File Path"]))
                else:
                    st.success("✅ No missing assets found.")
            
            with tab2:
                if delta.get('modified'):
                    st.warning("The following files have DIFFERENT content between environments:")
                    st.table(pd.DataFrame(delta['modified'], columns=["File Path"]))
                else:
                    st.success("✅ Content matches perfectly.")

            with tab3:
                st.info("Dependency Mapping Visualizer")
                try:
                    import graphviz
                    # Check if graphviz executable is in path by trying a simple graph
                    try:
                        # Simple check object
                        test_graph = graphviz.Digraph()
                        # We don't render it yet, just creating object is usually fine, 
                        # but rendering requires dot executable.
                        # Let's assume if import works, we try.
                        
                        graph = graphviz.Digraph()
                        
                        # Create graph from dependencies
                        has_deps = False
                        for path, asset in source_data.items():
                            if hasattr(asset, 'metadata') and 'dependencies' in asset.metadata:
                                has_deps = True
                                graph.node(path, shape='box')
                                for dep in asset.metadata['dependencies']:
                                    graph.node(dep, style='filled', color='lightgrey')
                                    graph.edge(path, dep)
                        
                        if has_deps:
                            st.graphviz_chart(graph)
                        else:
                            st.info("No dependencies found in source assets.")
                            
                    except Exception as e:
                         st.warning("Graphviz executable not found. Dependency graph cannot be rendered.")
                         st.caption(f"Error: {e}")
                         st.caption("Please install Graphviz system binaries (not just the python package) to view this graph.")

                except ImportError:
                    st.warning("Graphviz library not installed.")
                    
            with tab4:
                st.error("Shadow IT Discovery")
                shadow_items = []
                for path, asset in source_data.items():
                    if hasattr(asset, 'metadata') and asset.metadata.get('shadow_it_flag'):
                        shadow_items.append({
                            "File": path,
                            "Reason": asset.metadata.get('shadow_reason'),
                            "Size": asset.metadata.get('size')
                        })
                
                if shadow_items:
                    st.warning(f"Found {len(shadow_items)} unmanaged/suspicious items:")
                    st.table(pd.DataFrame(shadow_items))
                else:
                    st.success("No Shadow IT assets detected.")
                    
            # Export
            st.download_button(
                label="📥 Download Audit JSON",
                data=json.dumps(report, indent=2),
                file_name="p1_audit_report.json",
                mime="application/json"
            )

        except Exception as e:
            st.error(f"Error running audit: {e}")

render_footer()
