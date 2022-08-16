<?php

namespace App\Http\Resources;

use App\Models\Votesneighborhood;
use Illuminate\Http\Resources\Json\JsonResource;


class VotesNeighborhoodResource extends JsonResource
{
    /**
     * Transform the resource into an array.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return array|\Illuminate\Contracts\Support\Arrayable|\JsonSerializable
     */
    public function toArray($request)
    {

        return [
            'candidate' => CandidateResource::collection($this->whenLoaded('candidate')),

        ];
        //"NM_VOTAVEL","NR_VOTAVEL","ANO_ELEICAO","DS_CARGO_PERGUNTA","NM_MUNICIPIO","NM_BAIRRO","QT_VOTOS"
    }
}
