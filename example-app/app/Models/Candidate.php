<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Candidate extends Model
{
    use HasFactory;
    protected $table = 'candidates';  // NM_URNA_CANDIDATO
    protected $primaryKey = 'NM_URNA_CANDIDATO';
    public $incrementing = false;
    protected $keyType = 'string';

    public function getRouteKeyName()
    {
        return 'NM_URNA_CANDIDATO';
    }

    public function bairro2020() :HasMany
    {
       return $this->hasMany(Votesneighborhood::class,'NM_VOTAVEL')
       ->select("NM_VOTAVEL","NR_VOTAVEL","ANO_ELEICAO","DS_CARGO_PERGUNTA","NM_MUNICIPIO","NM_BAIRRO","QT_VOTOS")
       ->orderByDesc('QT_VOTOS');
    }
    public function bairro2018() :HasMany
    {
        return $this->hasMany(Votesneighborhood_2018::class,'NM_VOTAVEL')
        ->select("NM_VOTAVEL","NR_VOTAVEL","ANO_ELEICAO","DS_CARGO_PERGUNTA","NM_MUNICIPIO","NM_BAIRRO","QT_VOTOS")
        ->orderByDesc('QT_VOTOS');
    }
    public function bairro2016() :HasMany
    {
        return $this->hasMany(Votesneighborhood_2016::class,'NM_VOTAVEL')
        ->select("NM_VOTAVEL","NR_VOTAVEL","DT_GERACAO_HH_GERACAO","DS_CARGO_PERGUNTA","NM_MUNICIPIO","NM_BAIRRO","QT_VOTOS")
        ->orderByDesc('QT_VOTOS');
    }
    public function bairro2014() :HasMany
    {
        return $this->hasMany(Votesneighborhood_2014::class,'NM_VOTAVEL')
        ->select("NM_VOTAVEL","NR_VOTAVEL","DT_GERACAO_HH_GERACAO","DS_CARGO_PERGUNTA","NM_MUNICIPIO","NM_BAIRRO","QT_VOTOS")
        ->orderByDesc('QT_VOTOS');
    }
    public function bairro2012() :HasMany
    {
        return $this->hasMany(Votesneighborhood_2012::class,'NM_VOTAVEL')// local key?= primary key
        ->select("NM_VOTAVEL","NR_VOTAVEL","DT_GERACAO_HH_GERACAO","DS_CARGO_PERGUNTA","NM_MUNICIPIO","NM_BAIRRO","QT_VOTOS")
        ->orderByDesc('QT_VOTOS');
    }
    public function schools2020() :HasMany
    {
        return $this->hasMany(VotesSchools_2020::class,'NM_VOTAVEL')
        ->select("NM_VOTAVEL","NR_VOTAVEL","DT_GERACAO_HH_GERACAO","DS_CARGO_PERGUNTA","NM_MUNICIPIO","QT_VOTOS")
        ->orderByDesc('QT_VOTOS');
    }
    public function schools2018() :HasMany
    {
        return $this->hasMany(VotesSchools_2018::class,'NM_VOTAVEL')
        ->select("NM_VOTAVEL","NR_VOTAVEL","DT_GERACAO_HH_GERACAO","DS_CARGO_PERGUNTA","NM_MUNICIPIO","QT_VOTOS")
        ->orderByDesc('QT_VOTOS');
    }
    public function schools2016() :HasMany
    {
        return $this->hasMany(VotesSchools_2016::class,'NM_VOTAVEL')
        ->select("NM_VOTAVEL","NR_VOTAVEL","DT_GERACAO_HH_GERACAO","DS_CARGO_PERGUNTA","NM_MUNICIPIO","QT_VOTOS")
        ->orderByDesc('QT_VOTOS');
    }
    public function schools2014() :HasMany
    {
        return $this->hasMany(VotesSchools_2014::class,'NM_VOTAVEL')
        ->select("NM_VOTAVEL","NR_VOTAVEL","DT_GERACAO_HH_GERACAO","DS_CARGO_PERGUNTA","NM_MUNICIPIO","QT_VOTOS")
        ->orderByDesc('QT_VOTOS');
    }
    public function schools2012() :HasMany
    {
        return $this->hasMany(VotesSchools_2012::class,'NM_VOTAVEL')
        ->select("NM_VOTAVEL","NR_VOTAVEL","DT_GERACAO_HH_GERACAO","DS_CARGO_PERGUNTA","NM_MUNICIPIO","QT_VOTOS")
        ->orderByDesc('QT_VOTOS');
    }
    public function cities2020() :HasMany
    {
        return $this->hasMany(VotesCities_2020::class,'NM_VOTAVEL')
        ->select("NM_VOTAVEL","NR_VOTAVEL","DT_GERACAO_HH_GERACAO","DS_CARGO_PERGUNTA","NM_MUNICIPIO","QT_VOTOS")
        ->orderByDesc('QT_VOTOS');
    }
    public function cities2018() :HasMany
    {
        return $this->hasMany(VotesCities_2018::class,'NM_VOTAVEL')
        ->select("NM_VOTAVEL","NR_VOTAVEL","DT_GERACAO_HH_GERACAO","DS_CARGO_PERGUNTA","NM_MUNICIPIO","QT_VOTOS")
        ->orderByDesc('QT_VOTOS');
    }
    public function cities2016() :HasMany
    {
        return $this->hasMany(VotesCities_2016::class,'NM_VOTAVEL')
        ->select("NM_VOTAVEL","NR_VOTAVEL","DT_GERACAO_HH_GERACAO","DS_CARGO_PERGUNTA","NM_MUNICIPIO","QT_VOTOS")
        ->orderByDesc('QT_VOTOS');
    }
    public function cities2014() :HasMany
    {
        return $this->hasMany(VotesCities_2014::class,'NM_VOTAVEL')
        ->select("NM_VOTAVEL","NR_VOTAVEL","DT_GERACAO_HH_GERACAO","DS_CARGO_PERGUNTA","NM_MUNICIPIO","QT_VOTOS")
        ->orderByDesc('QT_VOTOS');
    }
    public function cities2012() :HasMany
    {
        return $this->hasMany(VotesCities_2012::class,'NM_VOTAVEL')
        ->select("NM_VOTAVEL","NR_VOTAVEL","DT_GERACAO_HH_GERACAO","DS_CARGO_PERGUNTA","NM_MUNICIPIO","QT_VOTOS")
        ->orderByDesc('QT_VOTOS');
    }


    public function scopeSearch($query, string $terms = null)
    {

            collect(explode(' ', $terms))->filter()->each(function ($term) use ($query) {
                $term = '%'.$term.'%';
                $query->where(function ($query) use ($term) {
                    $query->where('NM_CANDIDATO', 'ilike', $term)
                        ->orWhere('NM_URNA_CANDIDATO', 'ilike', $term)
                        ->orWhere('NR_CPF_CANDIDATO', 'ilike', $term);
                        // ->orWhereHas('user', function ($query) use ($term) {
                        //     $query->where('city', 'ilike', $term);
                        // });
                });
            });

    }
}
