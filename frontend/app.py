import streamlit as st

def main():
    st.set_page_config(page_title="NASA System Engineering Workflow", layout="wide")
    st.title("NASA System Engineering Workflow")

    tabs = st.tabs([
        "ConOps",
        "Design",
        "Development",
        "Operations",
        "Maintenance",
        "Closeout"
    ])

    with tabs[0]:
        conops_tab()

    with tabs[1]:
        design_tab()

    with tabs[2]:
        development_tab()

    with tabs[3]:
        operations_tab()

    with tabs[4]:
        maintenance_tab()

    with tabs[5]:
        closeout_tab()

def conops_tab():
    st.header("Concept of Operations (ConOps)")
    
    # Create two columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("Define the overall concept and objectives of the system.")
        
        mission_objective = st.text_area("Mission Objective")
        stakeholders = st.text_input("Key Stakeholders")
        operational_scenarios = st.text_area("Operational Scenarios")

        if st.button("Save ConOps"):
            # Here you would typically save this data
            st.success("ConOps information saved!")

    with col2:
        try:
            with open("backend/data/nasa/guidelines/ConOps.md", "r") as file:
                guidelines = file.read()
            st.markdown(guidelines)
        except FileNotFoundError:
            st.error("ConOps guidelines file not found. Please check the file path.")

def design_tab():
    st.header("Design")
    st.write("Create the system design based on the ConOps.")
    
    system_architecture = st.text_area("System Architecture")
    subsystems = st.text_area("Subsystems")
    interfaces = st.text_area("Interfaces")

    if st.button("Save Design"):
        st.success("Design information saved!")

def development_tab():
    st.header("Development")
    st.write("Implement the system based on the design.")
    
    development_plan = st.text_area("Development Plan")
    milestones = st.text_area("Key Milestones")
    risks = st.text_area("Identified Risks")

    if st.button("Save Development Info"):
        st.success("Development information saved!")

def operations_tab():
    st.header("Operations")
    st.write("Manage the operational phase of the system.")
    
    operational_procedures = st.text_area("Operational Procedures")
    performance_metrics = st.text_area("Performance Metrics")
    incident_response = st.text_area("Incident Response Plan")

    if st.button("Save Operations Info"):
        st.success("Operations information saved!")

def maintenance_tab():
    st.header("Maintenance")
    st.write("Maintain and update the system as needed.")
    
    maintenance_schedule = st.text_area("Maintenance Schedule")
    upgrade_plans = st.text_area("Upgrade Plans")
    support_procedures = st.text_area("Support Procedures")

    if st.button("Save Maintenance Info"):
        st.success("Maintenance information saved!")

def closeout_tab():
    st.header("Closeout")
    st.write("Conclude the project and document lessons learned.")
    
    final_report = st.text_area("Final Report")
    lessons_learned = st.text_area("Lessons Learned")
    future_recommendations = st.text_area("Future Recommendations")

    if st.button("Save Closeout Info"):
        st.success("Closeout information saved!")

if __name__ == "__main__":
    main()
