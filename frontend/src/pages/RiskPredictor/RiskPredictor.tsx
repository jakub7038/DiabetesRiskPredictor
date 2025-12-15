import React, { useState } from 'react';
// IMPORTUJEMY JAKO OBIEKT styles
import styles from './RiskPredictor.module.css';

interface Option {
    label: string;
    value: string;
}

interface QuestionConfig {
    id: string;
    text: string;
    type: 'select' | 'number';
    options?: Option[];
    unit?: string;        
    min?: number;         
    max?: number;         
}

interface StepConfig {
    id: number;
    stepLabel: string;
    title: string;
    description?: string;
    questions: QuestionConfig[];
}

const STEPS: StepConfig[] = [
    {
        id: 1,
        stepLabel: 'O Tobie',
        title: "Podstawowe informacje",
        description: "Wypełnij podstawowe informacje.",
        questions: [
            {
                id: 'gender',
                text: "Jaka jest Twoja płeć?",
                type: 'select',
                options: [
                    { label: "Kobieta", value: "0" },
                    { label: "Mężczyzna", value: "1" }
                ]
            },
            {
                id: 'age',
                text: "Wybierz przedział wiekowy",
                type: 'select',
                options: [
                    { label: "18-24", value: "1" },
                    { label: "25-29", value: "2" },
                    { label: "30-34", value: "3" },
                    { label: "35-39", value: "4" },
                    { label: "40-44", value: "5" },
                    { label: "45-49", value: "6" },
                    { label: "50-54", value: "7" },
                    { label: "55-59", value: "8" },
                    { label: "60-64", value: "9" },
                    { label: "65-69", value: "10" },
                    { label: "70-74", value: "11" },
                    { label: "75-79", value: "12" },
                    { label: "ponad 80", value: "13" },
                ]
            },

            {
                id: 'height',
                text: "Podaj swój wzrost w cm",
                type: "number",

            },
            {
                id: 'weight',
                text: "Jaka jest Twoja waga?",
                type: 'number',
                unit: 'kg',
            }

        ]
    },
    {
        id: 2,
        stepLabel: 'Stan zdrowia',
        title: "Aktualny stan zdrowia",
        questions: [
            {
                id: 'HighBP',
                text: "Czy w ostatnim czasie miałeś zmierzone wysokie ciśnienie ?",
                type: "select",
                options: [
                    { label: "Tak", value: "1" },
                    { label: "Nie", value: "0" }
                ]
            },
            {
                id: 'HighChol',
                text: "Czy w ostatnim czasie miałeś zmierzony wysoki choresterol ?",
                type: "select",
                options: [
                    { label: "Tak", value: "1" },
                    { label: "Nie", value: "0" }
                ]
            },
            {
                id: 'Stroke',
                text: "Czy kiedykolwiek miałeś udar ?",
                type: "select",
                options: [
                    { label: "Tak", value: "1" },
                    { label: "Nie", value: "0" }
                ]
            },
            {
                id: 'DiffWalk',
                text: "Czy posiadasz jakiekolwiek trudności z chodzeniem ?",
                type: "select",
                options: [
                    { label: "Tak", value: "1" },
                    { label: "Nie", value: "0" }
                ]
            },
            {
                id: 'GenHlth',
                text: "Jak oceniasz swój stan zdrowia ?",
                type: "select",
                options: [
                    { label: "Tragicznie", value: "1" },
                    { label: "Źle", value: "2" },
                    { label: "Może być", value: "3" },
                    { label: "Dobrze", value: "4" },
                    { label: "Doskonale", value: "5" }
                ]
            },
            {
                id: 'PhysHlth',
                text: "W ciągu ostatni 30 dni przez ile dni czułeś się dobrze pod względem fizycznym ?",
                type: 'number',
                unit: 'whatever',
                min: 0,
                max: 30
            }
        ]
    },
    {
        id: 3,
        stepLabel: 'Nawyki',
        title: "Twoje codzienne nawyki",
        questions: [
            {
                id: 'PhysActivity',
                text: "Czy uprawiasz jakąkolwiek aktywności fizyczną ?",
                type: "select",
                options: [
                    { label: "Tak", value: "1" },
                    { label: "Nie", value: "0" }
                ]
            },
            {
                id: 'Smoker',
                text: "Czy palisz papierosy ?",
                type: "select",
                options: [
                    { label: "Tak", value: "1" },
                    { label: "Nie", value: "0" }
                ]
            },
            {
                id: 'Fruits',
                text: "Czy spożywasz conajmniej jeden owoc dziennie ?",
                type: "select",
                options: [
                    { label: "Tak", value: "1" },
                    { label: "Nie", value: "0" }
                ]
            },
            {
                id: 'Veggies',
                text: "Czy spożywasz conajmniej jedno warzywo dzinnie ?",
                type: "select",
                options: [
                    { label: "Tak", value: "1" },
                    { label: "Nie", value: "0" }
                ]
            },
            {
                id: 'GenHlth',
                text: "Czy spożywasz dużo alkoholu ?",
                type: "select",
                options: [
                    { label: "Tak", value: "1" },
                    { label: "Nie", value: "0" },
                ]
            },
            {
                id: 'MentHlth ',
                text: "W ciągu ostatni 30 dni przez ile dni czułeś się dobrze pod względem zdrowia mentalnego ?",
                type: 'number',
                unit: 'whatever',
                min: 0,
                max: 30
            }
        ]
    }
];

const RiskPredictor = () => {
    const [currentStepIndex, setCurrentStepIndex] = useState(0);

    const [answers, setAnswers] = useState<Record<string, string | undefined>>({});

    const currentStep = STEPS[currentStepIndex];
    const isFirstStep = currentStepIndex === 0;
    const isLastStep = currentStepIndex === STEPS.length - 1;

    const handleNext = () => {
        if (!isLastStep) setCurrentStepIndex(prev => prev + 1);
    };

    const handleBack = () => {
        if (!isFirstStep) setCurrentStepIndex(prev => prev - 1);
    };


    const handleAnswerChange = (questionId: string, value: string) => {
        const finalValue = value.trim() === '' ? undefined : value;
        setAnswers(prev => ({ ...prev, [questionId]: finalValue }));

    };

    const allQuestionsAnswered = currentStep.questions.every(q => {
        const ans = answers[q.id];
        return ans !== undefined && ans !== '';
    });

    const handleSubmit = () => {
        // Do zrobienia 
        console.log(answers);

    };

    return (
        <div className={styles.formContainer}>

            {/* PASEK POSTĘPU */}
            <div className={styles.progressBarWrapper}>
                <div className={styles.progressLine}></div>
                <div className={styles.stepsContainer}>
                    {STEPS.map((step, index) => {
                        const isActive = index === currentStepIndex;
                        const isCompleted = index < currentStepIndex;
                        return (
                            <div key={step.id} className={styles.stepItem}>
                                <div className={`${styles.stepCircle} ${isActive ? styles.active : ''} ${isCompleted ? styles.completed : ''}`}>
                                    {isCompleted ? '✓' : step.id}
                                </div>
                                <span className={`${styles.stepLabel} ${isActive ? styles.activeText : ''}`}>
                                    {step.stepLabel}
                                </span>
                            </div>
                        );
                    })}
                </div>
            </div>

            <div className={styles.formContent}>

                <div className={styles.questionColumn}>
                    <div className={styles.stepInfo}>
                        <h2 className={styles.stepTitle}>{currentStep.title}</h2>
                        {currentStep.description && (
                            <p className={styles.stepDescription}>{currentStep.description}</p>
                        )}
                    </div>


                    <div className={styles.questionsList}>
                        {currentStep.questions.map((question) => (
                            <div key={question.id} className={styles.singleQuestionBlock}>

                                <h3 className={styles.questionText}>{question.text}</h3>

                                {question.type === 'select' && question.options && (
                                    <div className={styles.optionsGrid}>
                                        {question.options.map((option) => {
                                            const isSelected = answers[question.id] === option.value;
                                            return (
                                                <button
                                                    key={option.value}
                                                    className={`${styles.optionCard} ${isSelected ? styles.optionCardSelected : ''}`}
                                                    onClick={() => handleAnswerChange(question.id, option.value)}
                                                >
                                                    {option.label}
                                                </button>
                                            );
                                        })}
                                    </div>
                                )}


                                {question.type === 'number' && (
                                    <div className={styles.numberInputWrapper}>
                                        <input
                                            type="number"
                                            className={styles.numberInput}
                                            value={answers[question.id] || ''} 
                                            onChange={(e) => handleAnswerChange(question.id, e.target.value)}
                                            min={question.min}
                                            max={question.max}
                                            placeholder="Wpisz wartość"
                                        />
                                        {question.unit && <span className={styles.numberUnit}>{question.unit}</span>}
                                    </div>
                                )}

                            </div>
                        ))}
                    </div>

                     {/* NAWIGACJA */}
                    <div className={styles.footerNav}>
                        <button
                            className={`${styles.navBtn} ${styles.navBtnBack}`}
                            onClick={handleBack}
                            disabled={isFirstStep}
                            style={{ visibility: isFirstStep ? 'hidden' : 'visible' }} 
                        >
                            ←
                        </button>

                        {isLastStep ? (
                            <button
                                className={styles.submitBtn}
                                onClick={handleSubmit}
                                disabled={!allQuestionsAnswered}
                            >
                                Zakończ i wyślij
                            </button>
                        ) : (
                            <button
                                className={`${styles.navBtn} ${styles.navBtnNext}`}
                                onClick={handleNext}
                                disabled={!allQuestionsAnswered}
                            >
                                →
                            </button>
                        )}
                    </div>


                </div>
            </div>
        </div>
    );
};

export default RiskPredictor