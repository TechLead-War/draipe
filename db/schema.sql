SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: schema_migrations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.schema_migrations (
    version character varying(128) NOT NULL
);


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    id uuid NOT NULL,
    first_name character varying(50) NOT NULL,
    last_name character varying(50) NOT NULL,
    created_on timestamp with time zone DEFAULT now(),
    updated_on timestamp with time zone,
    email character varying(50) COLLATE pg_catalog."C",
    dob date NOT NULL,
    number character varying(10) NOT NULL,
    number_code character varying(3),
    gender character varying(1) NOT NULL COLLATE pg_catalog."C",
    status character varying(10) DEFAULT 'ACTIVE'::character varying NOT NULL,
    username character varying(50),
    premium_user boolean DEFAULT false,
    premium_buy_on timestamp without time zone,
    reference_id text DEFAULT true,
    password character varying(500) NOT NULL,
    deactivation_reason character varying(50) DEFAULT 'NOT_DEACTIVATED'::character varying NOT NULL,
    profile_picture character varying(255),
    address_id text,
    is_email_verified bigint,
    is_number_verified bigint,
    is_loyal_customer bigint,
    cart_id bigint,
    referral_id character varying(255)
);


--
-- Name: schema_migrations schema_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.schema_migrations
    ADD CONSTRAINT schema_migrations_pkey PRIMARY KEY (version);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users_email_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX users_email_idx ON public.users USING btree (lower((email)::text));


--
-- Name: users_number_ix; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX users_number_ix ON public.users USING btree (number);


--
-- PostgreSQL database dump complete
--


--
-- Dbmate schema migrations
--

INSERT INTO public.schema_migrations (version) VALUES
    ('20230406044451');
