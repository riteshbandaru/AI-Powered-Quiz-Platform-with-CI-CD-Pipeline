import streamlit as st
import os
from src.utils.helpers import QuizManager, rerun
from src.generator.question_generator import QuestionGenerator

# Set page configuration
st.set_page_config(
    page_title="*ZapStudy AI Quiz Generator*", 
    layout="centered",
    page_icon="📘"
)

# Initialize session state variables
if "questions_generated" not in st.session_state:
    st.session_state.questions_generated = False

if "show_results" not in st.session_state:
    st.session_state.show_results = False

if "quiz_manager" not in st.session_state:
    st.session_state.quiz_manager = QuizManager()

if "question_generator" not in st.session_state:
    st.session_state.question_generator = QuestionGenerator()

def main():
    st.title("📘 ZapStudy AI: Smart Question Generator")
    st.markdown("*Generate intelligent questions using AI for competitive exam preparation*")

    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configurations")
        
        # Input fields
        subject = st.text_input("Subject", "Computer Networks", help="Enter the subject name")
        topic = st.text_input("Topic", "TCP Congestion Control", help="Enter the specific topic")
        
        difficulty = st.selectbox(
            "Difficulty", 
            ["Easy", "Medium", "Hard"],
            index=1,
            help="Select difficulty level"
        )
        
        exam_type = st.selectbox(
            "Exam Type", 
            ["GATE", "JEE", "UGC-NET", "NEET", "CAT", "Custom"],
            help="Select the target exam type"
        )
        
        question_type = st.selectbox(
            "Question Type", 
            [
                "Multiple Choice",
                "Fill in the blank", 
                "Numeric",
                "True or False"
            ],
            help="Select the type of questions to generate"
        )
        
        num_questions = st.slider(
            "Number of Questions", 
            min_value=1, 
            max_value=10, 
            value=3,
            help="Select number of questions to generate"
        )

        # Generate questions button
        if st.button("🚀 Generate Questions", type="primary"):
            if not subject.strip():
                st.error("Please enter a subject name!")
                return
            
            if not topic.strip():
                st.error("Please enter a topic name!")
                return

            with st.spinner("🤖 Generating questions... Please wait!"):
                try:
                    success = st.session_state.quiz_manager.generate_questions(
                        generator=st.session_state.question_generator,
                        subject=subject.strip(),
                        topic=topic.strip(),
                        difficulty=difficulty,
                        question_type=question_type,
                        num_questions=num_questions,
                        exam_type=exam_type
                    )
                    
                    if success:
                        st.session_state.questions_generated = True
                        st.session_state.show_results = False
                        st.success(f"✅ Successfully generated {num_questions} questions!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to generate questions. Please try again.")
                        
                except Exception as e:
                    st.error(f"❌ Error generating questions: {str(e)}")

        # Reset button
        if st.session_state.questions_generated:
            if st.button("🔄 Reset Quiz", type="secondary"):
                st.session_state.questions_generated = False
                st.session_state.show_results = False
                st.session_state.quiz_manager = QuizManager()
                st.rerun()

    # Main content area
    if st.session_state.questions_generated:
        st.header("📝 Take the Quiz")
        st.markdown("Answer all questions and click **Submit Quiz** when you're done.")
        
        # Display questions
        with st.form("quiz_form"):
            st.session_state.quiz_manager.attempt_quiz()
            
            # Submit button
            submitted = st.form_submit_button("📊 Submit Quiz", type="primary")
            
            if submitted:
                # Check if all questions are answered
                all_answered = True
                for i, answer in enumerate(st.session_state.quiz_manager.user_answers):
                    if not answer or (isinstance(answer, str) and not answer.strip()):
                        all_answered = False
                        break
                
                if not all_answered:
                    st.error("⚠️ Please answer all questions before submitting!")
                else:
                    with st.spinner("📊 Evaluating your answers..."):
                        st.session_state.quiz_manager.evaluate_quiz()
                        st.session_state.show_results = True
                        st.success("✅ Quiz submitted successfully!")
                        st.rerun()

    elif not st.session_state.questions_generated and not st.session_state.show_results:
        # Welcome screen
        st.markdown("""
        ## Welcome to ZapStudy AI! 🎯
        
        **Features:**
        - 🤖 **AI-Powered Questions**: Generate intelligent questions using advanced language models
        - 📚 **Multiple Question Types**: MCQ, Fill-in-the-blanks, Numerical, True/False
        - 🎓 **Exam-Specific**: Tailored for GATE, JEE, UGC-NET, and more
        - 📊 **Instant Results**: Get detailed explanations and performance analysis
        - 💾 **Export Results**: Download your quiz results as CSV
        
        ### How to Use:
        1. **Configure** your preferences in the sidebar
        2. **Generate** questions by clicking the button
        3. **Take** the quiz by answering all questions
        4. **Review** your results with detailed explanations
        
        **Get started by filling in the configuration in the sidebar! →**
        """)

    # Results section
    if st.session_state.show_results:
        st.header("📈 Quiz Results")
        
        df = st.session_state.quiz_manager.generate_result_dataframe()
        
        if not df.empty:
            # Calculate score
            total_questions = len(df)
            correct_answers = df['is_correct'].sum()
            score_percentage = (correct_answers / total_questions) * 100
            
            # Display score summary
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Questions", total_questions)
            with col2:
                st.metric("Correct Answers", correct_answers)
            with col3:
                st.metric("Score", f"{score_percentage:.1f}%")
            
            # Performance indicator
            if score_percentage >= 80:
                st.success("🎉 Excellent performance! Keep it up!")
            elif score_percentage >= 60:
                st.info("👍 Good job! There's room for improvement.")
            else:
                st.warning("📖 Keep practicing! Review the explanations below.")
            
            st.markdown("---")
            
            # Detailed results
            st.subheader("📋 Detailed Results")
            
            for i, row in df.iterrows():
                with st.expander(f"Question {row['question_number']}: {'✅' if row['is_correct'] else '❌'}", expanded=False):
                    st.markdown(f"**{row['question']}**")
                    
                    if row['type'] == 'MCQ' and row['options']:
                        st.markdown("**Options:**")
                        for j, option in enumerate(row['options'], 1):
                            st.markdown(f"{j}. {option}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**Your Answer:** `{row['user_answer']}`")
                    with col2:
                        st.markdown(f"**Correct Answer:** `{row['correct_answer']}`")
                    
                    st.markdown(f"**Explanation:** {row['explanation']}")
                    
                    if row['is_correct']:
                        st.success("✅ Correct!")
                    else:
                        st.error("❌ Incorrect")
            
            # Download results
            st.markdown("---")
            st.subheader("📥 Export Results")
            
            try:
                csv_path = st.session_state.quiz_manager.save_to_csv()
                if csv_path and os.path.exists(csv_path):
                    with open(csv_path, "rb") as file:
                        st.download_button(
                            label="⬇️ Download Results as CSV",
                            data=file,
                            file_name=os.path.basename(csv_path),
                            mime="text/csv",
                            help="Download your quiz results for future reference"
                        )
            except Exception as e:
                st.error(f"Error saving results: {str(e)}")

if __name__ == "__main__":
    main()
