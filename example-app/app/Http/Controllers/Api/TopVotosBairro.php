<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Resources\VotesBairro2020;
use App\Models\Votesneighborhood;
use App\Models\Votesneighborhood_2012;
use App\Models\Votesneighborhood_2014;
use App\Models\Votesneighborhood_2016;
use App\Models\Votesneighborhood_2018;
use Illuminate\Http\Request;

class TopVotosBairro extends Controller
{
    public function BairroMaisVotada()
    {

        if(request()->get('top_bairro')){
            if(request()->get('top_bairro') == 'bairro2020'){
                $option = Votesneighborhood::class;
            }else if(request()->get('top_bairro') == 'bairro2018'){
                $option = Votesneighborhood_2018::class;
            }else if(request()->get('top_bairro') == 'bairro2016'){
                $option = Votesneighborhood_2016::class;
            }else if(request()->get('top_bairro') == 'bairro2014'){
                $option = Votesneighborhood_2014::class;
            }else if(request()->get('top_bairro') == 'bairro2012'){
                $option = Votesneighborhood_2012::class;
            }else
                {
                    return 'Informe bairro.. ex: bairro2014';
                }

            if(request()->has('top_bairro','amount')){

                $var = $option::orderBy('QT_VOTOS','desc')
                ->whereNotIn('NM_VOTAVEL',['NULO','BRANCO'])
                ->when(request()->get('municipio'),function($query){
                    $query->where('NM_MUNICIPIO',request()->get('municipio'));
                })
                ->when(request()->get('bairro'),function($query){
                    $query->where('NM_BAIRRO',request()->get('bairro'));
                })
                ->when(request()->get('cargo'),function($query){
                    $query->where('DS_CARGO_PERGUNTA',request()->get('cargo'));
                })
                ->when(request()->only('top_bairro'),function($query){
                    return $query->take(1000);
                })
                ->get();

                return VotesBairro2020::collection($var->unique('NM_VOTAVEL')->take(request()->get('amount')));

            }

        }
        else{
            return 'NO DATA';
        }
    }
}

