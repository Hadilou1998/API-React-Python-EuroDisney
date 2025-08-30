type Props = { label: string; children: React.ReactNode };

export default function FormField({ label, children }: Props) {
    return (
        <div className="form-field">
            <label className="form-label">{label}</label>
            {children}
        </div>
    )
};