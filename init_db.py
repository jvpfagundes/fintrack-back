""""""

"""CREATE TABLE IF NOT EXISTS users (
        id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
        phone_number VARCHAR(255) UNIQUE NOT NULL,
        hashed_password VARCHAR(255) NOT NULL,
        first_name VARCHAR(255),
        last_name VARCHAR(255),
        birth_date DATE,
        monthly_goal FLOAT,
        daily_goal FLOAT,
        theme VARCHAR(255),
        is_first_access BOOLEAN DEFAULT TRUE,
        status BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        deleted_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        username varchar(255),
        language VARCHAR(255)
    );
-- Tabela de categorias de despesa
CREATE TABLE expense_category (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(200) NOT NULL,
    status BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ,
    deleted_at TIMESTAMPTZ,
    user_id uuid 
    
        CONSTRAINT fk_category_user FOREIGN KEY (user_id)
        REFERENCES users (id) ON DELETE NO ACTION,
);

-- Tabela de despesas
CREATE TABLE expenses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    value DECIMAL(14,2) NOT NULL,
    category_id UUID NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ,
    deleted_at TIMESTAMPTZ,
    expense_date DATE NOT NULL,
    expense_time TIME NOT NULL,

    CONSTRAINT fk_expenses_user FOREIGN KEY (user_id)
        REFERENCES users (id) ON DELETE NO ACTION,

    CONSTRAINT fk_expenses_category FOREIGN KEY (category_id)
        REFERENCES expense_category (id) ON DELETE NO ACTION
);
"""